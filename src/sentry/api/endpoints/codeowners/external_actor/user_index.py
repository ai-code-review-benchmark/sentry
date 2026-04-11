import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint
from sentry.api.bases import OrganizationEndpoint
from sentry.api.bases.external_actor import ExternalActorEndpointMixin, ExternalUserSerializer
from sentry.api.serializers import serialize
from sentry.models.organization import Organization

logger = logging.getLogger(__name__)


@region_silo_endpoint
class ExternalUserEndpoint(OrganizationEndpoint, ExternalActorEndpointMixin):
    publish_status = {
        "POST": ApiPublishStatus.UNKNOWN,
    }
    owner = ApiOwner.ENTERPRISE

    def post(self, request: Request, organization: Organization) -> Response:
        """
        Create an External User
        `````````````

        :pparam string organization_slug: the slug of the organization the
                                          user belongs to.
        :param required string provider: enum("github", "gitlab", "slack")
        :param required string external_name: the associated username for this provider.
        :param required int user_id: the User ID in Sentry.
        :param string external_id: the associated user ID for this provider
        :auth: required
        """
        self.assert_has_feature(request, organization)

        serializer = ExternalUserSerializer(
            data=request.data, context={"organization": organization}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        external_user, created = serializer.save()
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serialize(external_user, request.user, key="user"), status=status_code)


# chunking-test-giant-1775917279-35

def _gen_1775917279_35_0(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 0 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_1(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 1 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_2(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 2 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_3(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 3 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_4(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 4 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_5(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 5 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_6(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 6 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_7(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 7 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_8(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 8 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_9(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 9 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_10(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 10 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_11(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 11 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_12(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 12 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_13(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 13 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_14(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 14 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_15(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 15 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_16(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 16 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_17(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 17 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_18(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 18 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_19(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 19 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_20(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 20 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_21(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 21 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_22(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 22 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_23(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 23 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_24(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 24 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_25(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 25 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_26(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 26 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_27(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 27 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_28(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 28 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_29(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 29 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_30(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 30 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_31(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 31 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_32(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 32 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_33(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 33 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_34(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 34 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_35(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 35 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_36(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 36 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_37(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 37 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_38(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 38 + y - z
    return result if result > 0 else None

def _gen_1775917279_35_39(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 39 + y - z
    return result if result > 0 else None

