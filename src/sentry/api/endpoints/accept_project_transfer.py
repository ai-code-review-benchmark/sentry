from django.core.signing import BadSignature, SignatureExpired
from django.http import Http404
from django.utils.encoding import force_str
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from sentry import audit_log, roles
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import Endpoint, region_silo_endpoint
from sentry.api.decorators import sudo_required
from sentry.api.serializers import serialize
from sentry.api.serializers.models.organization import (
    DetailedOrganizationSerializerWithProjectsAndTeams,
)
from sentry.models.organization import Organization
from sentry.models.project import Project
from sentry.utils import metrics
from sentry.utils.signing import unsign


class InvalidPayload(Exception):
    pass


@region_silo_endpoint
class AcceptProjectTransferEndpoint(Endpoint):
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "POST": ApiPublishStatus.UNKNOWN,
    }
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_validated_data(self, data, user):
        try:
            data = unsign(force_str(data))
        except SignatureExpired:
            raise InvalidPayload("Project transfer link has expired.")
        except BadSignature:
            raise InvalidPayload("Could not approve transfer, please make sure link is valid.")

        if data["user_id"] != user.id:
            raise InvalidPayload("Invalid permissions")

        try:
            project = Project.objects.get(
                id=data["project_id"], organization_id=data["from_organization_id"]
            )
        except Project.DoesNotExist:
            raise InvalidPayload("Project no longer exists")

        return data, project

    @sudo_required
    def get(self, request: Request) -> Response:
        try:
            data = request.GET["data"]
        except KeyError:
            raise Http404

        try:
            data, project = self.get_validated_data(data, request.user)
        except InvalidPayload as e:
            return Response({"detail": str(e)}, status=400)

        organizations = Organization.objects.get_organizations_where_user_is_owner(
            user_id=request.user.id
        )

        return Response(
            {
                "organizations": serialize(
                    list(organizations),
                    request.user,
                    DetailedOrganizationSerializerWithProjectsAndTeams(),
                    access=request.access,
                ),
                "project": {"slug": project.slug, "id": project.id},
            }
        )

    @sudo_required
    def post(self, request: Request) -> Response:
        try:
            data = request.data["data"]
        except KeyError:
            raise Http404

        try:
            data, project = self.get_validated_data(data, request.user)
        except InvalidPayload as e:
            return Response({"detail": str(e)}, status=400)

        transaction_id = data["transaction_id"]

        org_slug = request.data.get("organization")
        # DEPRECATED
        team_id = request.data.get("team")

        if org_slug is None and team_id is not None:
            metrics.incr("accept_project_transfer.post.to_team")
            return Response({"detail": "Cannot transfer projects to a team."}, status=400)

        try:
            organization = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return Response({"detail": "Invalid organization"}, status=400)

        # check if user is an owner of the organization
        is_org_owner = request.access.has_role_in_organization(
            role=roles.get_top_dog().id, organization=organization, user_id=request.user.id
        )

        if not is_org_owner:
            return Response({"detail": "Invalid organization"}, status=400)

        project.transfer_to(organization=organization)

        self.create_audit_entry(
            request=request,
            organization=project.organization,
            target_object=project.id,
            event=audit_log.get_event_id("PROJECT_ACCEPT_TRANSFER"),
            data=project.get_audit_log_data(),
            transaction_id=transaction_id,
        )

        return Response(status=204)


# chunking-test-marker-1775914323-1


# chunking-test-v3-1775914457-1


# chunking-test-big-1775914536-1

def _generated_function_1775914536_1_0(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 0 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_1(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 1 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_2(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 2 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_3(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 3 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_4(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 4 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_5(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 5 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_6(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 6 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_7(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 7 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_8(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 8 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_9(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 9 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_10(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 10 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_11(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 11 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_12(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 12 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_13(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 13 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_14(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 14 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_15(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 15 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_16(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 16 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_17(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 17 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_18(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 18 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_19(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 19 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_20(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 20 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_21(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 21 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_22(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 22 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_23(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 23 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_24(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 24 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_25(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 25 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_26(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 26 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_27(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 27 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_28(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 28 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_29(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 29 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_30(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 30 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_31(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 31 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_32(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 32 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_33(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 33 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_34(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 34 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_35(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 35 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_36(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 36 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_37(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 37 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_38(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 38 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_39(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 39 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_40(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 40 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_41(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 41 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_42(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 42 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_43(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 43 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_44(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 44 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_45(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 45 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_46(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 46 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_47(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 47 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_48(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 48 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_49(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 49 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_50(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 50 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_51(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 51 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_52(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 52 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_53(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 53 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_54(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 54 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_55(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 55 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_56(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 56 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_57(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 57 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_58(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 58 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_1_59(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 59 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

