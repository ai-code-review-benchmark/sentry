from __future__ import annotations

import logging
from collections.abc import Mapping

from django.http import HttpRequest
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import Endpoint, control_silo_endpoint
from sentry.api.invite_helper import (
    ApiInviteHelper,
    add_invite_details_to_session,
    remove_invite_details_from_session,
)
from sentry.models.authprovider import AuthProvider
from sentry.models.organizationmapping import OrganizationMapping
from sentry.models.organizationmembermapping import OrganizationMemberMapping
from sentry.services.hybrid_cloud.organization import (
    RpcUserInviteContext,
    RpcUserOrganizationContext,
    organization_service,
)
from sentry.types.region import RegionResolutionError, get_region_by_name
from sentry.utils import auth

logger = logging.getLogger(__name__)


def get_invite_state(
    member_id: int,
    organization_slug: str | None,
    user_id: int,
    request: HttpRequest,
) -> RpcUserInviteContext | None:
    if organization_slug is None:
        member_mapping: OrganizationMemberMapping | None = None
        member_mappings: Mapping[int, OrganizationMemberMapping] = {
            omm.organization_id: omm
            for omm in OrganizationMemberMapping.objects.filter(
                organizationmember_id=member_id
            ).all()
        }
        org_mappings = OrganizationMapping.objects.filter(
            organization_id__in=list(member_mappings.keys())
        )
        for mapping in org_mappings:
            try:
                if get_region_by_name(mapping.region_name).is_historic_monolith_region():
                    member_mapping = member_mappings.get(mapping.organization_id)
                    break
            except RegionResolutionError:
                pass

        if member_mapping is None:
            return None
        invite_context = organization_service.get_invite_by_id(
            organization_id=member_mapping.organization_id,
            organization_member_id=member_id,
            user_id=user_id,
        )

        logger.info(
            "organization.member_invite.no_slug",
            extra={
                "member_id": member_id,
                "org_id": member_mapping.organization_id,
                "url": request.path,
                "method": request.method,
            },
        )
    else:
        invite_context = organization_service.get_invite_by_slug(
            organization_member_id=member_id,
            slug=organization_slug,
            user_id=user_id,
        )

    return invite_context


@control_silo_endpoint
class AcceptOrganizationInvite(Endpoint):
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "POST": ApiPublishStatus.UNKNOWN,
    }
    # Disable authentication and permission requirements.
    permission_classes = ()

    @staticmethod
    def respond_invalid() -> Response:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"details": "Invalid invite code"})

    def get_helper(
        self, request: Request, token: str, invite_context: RpcUserOrganizationContext
    ) -> ApiInviteHelper:
        return ApiInviteHelper(request=request, token=token, invite_context=invite_context)

    def get(
        self, request: Request, member_id: int, token: str, organization_slug: str | None = None
    ) -> Response:
        invite_context = get_invite_state(
            member_id=int(member_id),
            organization_slug=organization_slug,
            user_id=request.user.id,
            request=request,
        )
        if invite_context is None:
            return self.respond_invalid()

        helper = self.get_helper(request, token, invite_context)

        organization_member = invite_context.member
        organization = invite_context.organization

        if (
            not helper.member_pending
            or not helper.valid_token
            or not organization_member.invite_approved
        ):
            return self.respond_invalid()

        # Keep track of the invite details in the request session
        request.session["invite_email"] = organization_member.email

        try:
            auth_provider = AuthProvider.objects.get(organization_id=organization.id)
        except AuthProvider.DoesNotExist:
            auth_provider = None

        data = {
            "orgSlug": organization.slug,
            "needsAuthentication": not helper.user_authenticated,
            "needsSso": auth_provider is not None,
            "hasAuthProvider": auth_provider is not None,
            "requireSso": auth_provider is not None and not auth_provider.flags.allow_unlinked,
            # If they're already a member of the organization its likely
            # they're using a shared account and either previewing this invite
            # or are incorrectly expecting this to create a new account.
            "existingMember": helper.member_already_exists,
        }

        response = Response(None)

        # Allow users to register an account when accepting an invite
        if not helper.user_authenticated:
            request.session["can_register"] = True
            add_invite_details_to_session(
                request,
                organization_member.id,
                organization_member.token,
                invite_context.organization.id,
            )

            # When SSO is required do *not* set a next_url to return to accept
            # invite. The invite will be accepted after SSO is completed.
            url = (
                reverse("sentry-accept-invite", args=[member_id, token])
                if not auth_provider
                else "/"
            )
            auth.initiate_login(self.request, next_url=url)

        # If the org has SSO setup, we'll store the invite cookie to later
        # associate the org member after authentication. We can avoid needing
        # to come back to the accept invite page since 2FA will *not* be
        # required if SSO is required.
        if auth_provider is not None:
            add_invite_details_to_session(
                request,
                organization_member.id,
                organization_member.token,
                organization_member.organization_id,
            )

            provider = auth_provider.get_provider()
            data["ssoProvider"] = provider.name

        onboarding_steps = helper.get_onboarding_steps()
        data.update(onboarding_steps)
        if any(onboarding_steps.values()):
            add_invite_details_to_session(
                request,
                organization_member.id,
                organization_member.token,
                invite_context.organization.id,
            )

        response.data = data

        return response

    def post(
        self, request: Request, member_id: int, token: str, organization_slug: str | None = None
    ) -> Response:
        invite_context = get_invite_state(
            member_id=int(member_id),
            organization_slug=organization_slug,
            user_id=request.user.id,
            request=request,
        )
        if invite_context is None:
            return self.respond_invalid()

        helper = self.get_helper(request, token, invite_context)

        if helper.member_already_exists:
            response = Response(
                status=status.HTTP_400_BAD_REQUEST, data={"details": "member already exists"}
            )
        elif not helper.valid_request:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"details": "unable to accept organization invite"},
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT)

        helper.accept_invite()
        remove_invite_details_from_session(request)

        return response


# chunking-test-marker-1775914323-0


# chunking-test-v3-1775914457-0


# chunking-test-big-1775914536-0

def _generated_function_1775914536_0_0(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 0 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_1(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 1 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_2(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 2 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_3(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 3 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_4(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 4 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_5(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 5 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_6(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 6 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_7(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 7 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_8(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 8 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_9(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 9 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_10(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 10 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_11(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 11 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_12(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 12 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_13(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 13 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_14(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 14 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_15(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 15 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_16(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 16 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_17(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 17 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_18(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 18 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_19(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 19 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_20(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 20 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_21(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 21 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_22(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 22 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_23(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 23 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_24(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 24 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_25(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 25 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_26(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 26 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_27(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 27 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_28(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 28 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_29(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 29 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_30(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 30 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_31(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 31 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_32(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 32 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_33(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 33 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_34(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 34 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_35(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 35 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_36(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 36 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_37(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 37 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_38(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 38 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_39(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 39 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_40(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 40 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_41(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 41 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_42(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 42 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_43(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 43 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_44(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 44 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_45(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 45 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_46(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 46 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_47(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 47 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_48(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 48 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_49(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 49 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_50(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 50 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_51(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 51 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_52(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 52 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_53(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 53 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_54(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 54 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_55(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 55 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_56(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 56 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_57(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 57 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_58(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 58 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_0_59(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 59 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

