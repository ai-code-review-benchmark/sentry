from django.db import router, transaction
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ListField

from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import Endpoint, control_silo_endpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.models.apiapplication import ApiApplication, ApiApplicationStatus
from sentry.models.scheduledeletion import ScheduledDeletion


class ApiApplicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    redirectUris = ListField(child=serializers.URLField(max_length=255), required=False)
    allowedOrigins = ListField(
        # TODO(dcramer): make this validate origins
        child=serializers.CharField(max_length=255),
        required=False,
    )
    homepageUrl = serializers.URLField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
    termsUrl = serializers.URLField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
    privacyUrl = serializers.URLField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )


@control_silo_endpoint
class ApiApplicationDetailsEndpoint(Endpoint):
    publish_status = {
        "DELETE": ApiPublishStatus.UNKNOWN,
        "GET": ApiPublishStatus.UNKNOWN,
        "PUT": ApiPublishStatus.UNKNOWN,
    }
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, app_id) -> Response:
        try:
            instance = ApiApplication.objects.get(
                owner_id=request.user.id, client_id=app_id, status=ApiApplicationStatus.active
            )
        except ApiApplication.DoesNotExist:
            raise ResourceDoesNotExist

        return Response(serialize(instance, request.user))

    def put(self, request: Request, app_id) -> Response:
        try:
            instance = ApiApplication.objects.get(
                owner_id=request.user.id, client_id=app_id, status=ApiApplicationStatus.active
            )
        except ApiApplication.DoesNotExist:
            raise ResourceDoesNotExist

        serializer = ApiApplicationSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            result = serializer.validated_data
            kwargs = {}
            if "name" in result:
                kwargs["name"] = result["name"]
            if "allowedOrigins" in result:
                kwargs["allowed_origins"] = "\n".join(result["allowedOrigins"])
            if "redirectUris" in result:
                kwargs["redirect_uris"] = "\n".join(result["redirectUris"])
            if "homepageUrl" in result:
                kwargs["homepage_url"] = result["homepageUrl"]
            if "privacyUrl" in result:
                kwargs["privacy_url"] = result["privacyUrl"]
            if "termsUrl" in result:
                kwargs["terms_url"] = result["termsUrl"]
            if kwargs:
                instance.update(**kwargs)
            return Response(serialize(instance, request.user), status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, app_id) -> Response:
        try:
            instance = ApiApplication.objects.get(
                owner_id=request.user.id, client_id=app_id, status=ApiApplicationStatus.active
            )
        except ApiApplication.DoesNotExist:
            raise ResourceDoesNotExist

        with transaction.atomic(using=router.db_for_write(ApiApplication)):
            updated = ApiApplication.objects.filter(id=instance.id).update(
                status=ApiApplicationStatus.pending_deletion
            )
            if updated:
                ScheduledDeletion.schedule(instance, days=0, actor=request.user)
        return Response(status=204)


# chunking-test-marker-1775914323-3


# chunking-test-v3-1775914457-3


# chunking-test-big-1775914536-3

def _generated_function_1775914536_3_0(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 0 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_1(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 1 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_2(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 2 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_3(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 3 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_4(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 4 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_5(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 5 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_6(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 6 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_7(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 7 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_8(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 8 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_9(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 9 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_10(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 10 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_11(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 11 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_12(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 12 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_13(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 13 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_14(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 14 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_15(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 15 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_16(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 16 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_17(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 17 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_18(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 18 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_19(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 19 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_20(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 20 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_21(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 21 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_22(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 22 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_23(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 23 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_24(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 24 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_25(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 25 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_26(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 26 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_27(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 27 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_28(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 28 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_29(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 29 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_30(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 30 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_31(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 31 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_32(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 32 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_33(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 33 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_34(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 34 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_35(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 35 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_36(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 36 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_37(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 37 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_38(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 38 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_39(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 39 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_40(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 40 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_41(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 41 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_42(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 42 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_43(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 43 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_44(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 44 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_45(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 45 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_46(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 46 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_47(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 47 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_48(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 48 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_49(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 49 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_50(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 50 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_51(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 51 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_52(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 52 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_53(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 53 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_54(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 54 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_55(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 55 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_56(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 56 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_57(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 57 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_58(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 58 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_3_59(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 59 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

