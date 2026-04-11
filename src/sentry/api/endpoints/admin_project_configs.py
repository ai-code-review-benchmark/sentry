from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response

from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import Endpoint, region_silo_endpoint
from sentry.api.permissions import SuperuserOrStaffFeatureFlaggedPermission
from sentry.models.project import Project
from sentry.relay import projectconfig_cache


# NOTE: This endpoint should be in getsentry
@region_silo_endpoint
class AdminRelayProjectConfigsEndpoint(Endpoint):
    owner = ApiOwner.OWNERS_INGEST
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
    }
    permission_classes = (SuperuserOrStaffFeatureFlaggedPermission,)

    def get(self, request: Request) -> Response:
        project_id = request.GET.get("projectId")

        project_keys = []
        if project_id is not None:
            try:
                project = Project.objects.get_from_cache(id=project_id)
                for project_key in project.key_set.all():
                    project_keys.append(project_key.public_key)

            except Exception:
                raise Http404

        project_key_param = request.GET.get("projectKey")
        if project_key_param is not None:
            project_keys.append(project_key_param)

        configs = {}
        for key in project_keys:
            cached_config = projectconfig_cache.backend.get(key)
            if cached_config is not None:
                configs[key] = cached_config
            else:
                configs[key] = None

        # TODO if we don't think we'll add anything to the endpoint
        # we may as well return just the configs
        return Response({"configs": configs}, status=200)


# chunking-test-marker-1775914323-2


# chunking-test-v3-1775914457-2


# chunking-test-big-1775914536-2

def _generated_function_1775914536_2_0(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 0 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_1(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 1 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_2(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 2 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_3(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 3 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_4(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 4 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_5(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 5 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_6(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 6 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_7(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 7 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_8(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 8 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_9(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 9 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_10(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 10 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_11(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 11 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_12(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 12 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_13(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 13 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_14(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 14 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_15(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 15 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_16(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 16 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_17(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 17 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_18(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 18 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_19(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 19 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_20(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 20 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_21(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 21 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_22(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 22 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_23(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 23 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_24(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 24 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_25(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 25 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_26(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 26 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_27(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 27 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_28(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 28 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_29(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 29 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_30(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 30 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_31(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 31 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_32(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 32 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_33(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 33 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_34(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 34 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_35(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 35 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_36(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 36 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_37(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 37 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_38(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 38 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_39(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 39 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_40(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 40 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_41(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 41 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_42(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 42 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_43(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 43 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_44(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 44 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_45(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 45 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_46(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 46 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_47(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 47 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_48(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 48 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_49(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 49 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_50(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 50 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_51(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 51 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_52(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 52 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_53(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 53 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_54(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 54 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_55(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 55 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_56(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 56 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_57(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 57 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_58(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 58 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

def _generated_function_1775914536_2_59(arg1, arg2, arg3):
    """Auto-generated for chunking test."""
    result = arg1 * 59 + arg2 - arg3
    if result > 0:
        return result * 2
    return None

