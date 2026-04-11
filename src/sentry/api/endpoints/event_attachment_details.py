import posixpath

from django.http import StreamingHttpResponse
from rest_framework.request import Request
from rest_framework.response import Response

from sentry import eventstore, features, roles
from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint
from sentry.api.bases.project import ProjectEndpoint, ProjectPermission
from sentry.api.serializers import serialize
from sentry.auth.superuser import superuser_has_permission
from sentry.auth.system import is_system_auth
from sentry.constants import ATTACHMENTS_ROLE_DEFAULT
from sentry.models.eventattachment import EventAttachment
from sentry.models.organizationmember import OrganizationMember


class EventAttachmentDetailsPermission(ProjectPermission):
    def has_object_permission(self, request: Request, view, project):
        result = super().has_object_permission(request, view, project)

        if not result:
            return result

        if is_system_auth(request.auth) or superuser_has_permission(request):
            return True

        if not request.user.is_authenticated:
            return False

        organization = project.organization
        required_role = (
            organization.get_option("sentry:attachments_role") or ATTACHMENTS_ROLE_DEFAULT
        )

        try:
            om = OrganizationMember.objects.get(organization=organization, user_id=request.user.id)
        except OrganizationMember.DoesNotExist:
            return False

        required_role = roles.get(required_role)
        om_role = roles.get(om.role)
        return om_role.priority >= required_role.priority


@region_silo_endpoint
class EventAttachmentDetailsEndpoint(ProjectEndpoint):
    owner = ApiOwner.PROCESSING
    publish_status = {
        "DELETE": ApiPublishStatus.UNKNOWN,
        "GET": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (EventAttachmentDetailsPermission,)

    def download(self, attachment):
        name = posixpath.basename(" ".join(attachment.name.split()))

        def stream_attachment():
            with attachment.getfile() as fp:
                while chunk := fp.read(4096):
                    yield chunk

        response = StreamingHttpResponse(
            stream_attachment(),
            content_type=attachment.content_type,
        )
        response["Content-Length"] = attachment.size
        response["Content-Disposition"] = f'attachment; filename="{name}"'

        return response

    def get(self, request: Request, project, event_id, attachment_id) -> Response:
        """
        Retrieve an Attachment
        ``````````````````````

        :pparam string organization_slug: the slug of the organization the
                                          issues belong to.
        :pparam string project_slug: the slug of the project the event
                                     belongs to.
        :pparam string event_id: the id of the event.
        :pparam string attachment_id: the id of the attachment.
        :auth: required
        """
        if not features.has(
            "organizations:event-attachments", project.organization, actor=request.user
        ):
            return self.respond(status=404)

        event = eventstore.backend.get_event_by_id(project.id, event_id)
        if event is None:
            return self.respond({"detail": "Event not found"}, status=404)

        try:
            attachment = EventAttachment.objects.filter(
                project_id=project.id, event_id=event.event_id, id=attachment_id
            ).get()
        except EventAttachment.DoesNotExist:
            return self.respond({"detail": "Attachment not found"}, status=404)

        if request.GET.get("download") is not None:
            return self.download(attachment)

        return self.respond(serialize(attachment, request.user))

    def delete(self, request: Request, project, event_id, attachment_id) -> Response:
        """
        Delete an Event Attachment by ID
        ````````````````````````````````

        Delete an attachment on the given event.

        :pparam string event_id: the identifier of the event.
        :pparam string attachment_id: the identifier of the attachment.
        :auth: required
        """
        if not features.has(
            "organizations:event-attachments", project.organization, actor=request.user
        ):
            return self.respond(status=404)

        try:
            attachment = EventAttachment.objects.filter(
                project_id=project.id, event_id=event_id, id=attachment_id
            ).get()
        except EventAttachment.DoesNotExist:
            return self.respond({"detail": "Attachment not found"}, status=404)

        attachment.delete()
        return self.respond(status=204)


# chunking-test-giant-1775917279-42

def _gen_1775917279_42_0(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 0 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_1(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 1 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_2(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 2 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_3(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 3 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_4(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 4 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_5(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 5 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_6(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 6 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_7(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 7 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_8(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 8 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_9(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 9 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_10(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 10 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_11(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 11 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_12(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 12 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_13(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 13 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_14(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 14 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_15(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 15 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_16(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 16 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_17(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 17 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_18(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 18 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_19(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 19 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_20(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 20 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_21(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 21 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_22(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 22 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_23(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 23 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_24(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 24 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_25(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 25 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_26(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 26 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_27(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 27 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_28(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 28 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_29(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 29 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_30(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 30 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_31(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 31 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_32(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 32 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_33(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 33 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_34(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 34 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_35(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 35 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_36(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 36 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_37(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 37 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_38(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 38 + y - z
    return result if result > 0 else None

def _gen_1775917279_42_39(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 39 + y - z
    return result if result > 0 else None



# chunking-test-giant-1775918140-42

def _gen_1775918140_42_0(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 0 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_1(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 1 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_2(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 2 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_3(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 3 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_4(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 4 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_5(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 5 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_6(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 6 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_7(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 7 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_8(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 8 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_9(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 9 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_10(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 10 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_11(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 11 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_12(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 12 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_13(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 13 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_14(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 14 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_15(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 15 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_16(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 16 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_17(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 17 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_18(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 18 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_19(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 19 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_20(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 20 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_21(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 21 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_22(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 22 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_23(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 23 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_24(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 24 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_25(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 25 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_26(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 26 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_27(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 27 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_28(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 28 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_29(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 29 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_30(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 30 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_31(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 31 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_32(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 32 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_33(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 33 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_34(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 34 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_35(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 35 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_36(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 36 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_37(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 37 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_38(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 38 + y - z
    return result if result > 0 else None

def _gen_1775918140_42_39(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 39 + y - z
    return result if result > 0 else None

