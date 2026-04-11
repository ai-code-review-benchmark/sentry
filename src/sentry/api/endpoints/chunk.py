import logging
import re
from gzip import GzipFile
from io import BytesIO

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from sentry import options
from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationReleasePermission
from sentry.api.utils import generate_region_url
from sentry.models.files.fileblob import FileBlob
from sentry.ratelimits.config import RateLimitConfig
from sentry.utils.files import get_max_file_size
from sentry.utils.http import absolute_uri

MAX_CHUNKS_PER_REQUEST = 64
MAX_REQUEST_SIZE = 32 * 1024 * 1024
MAX_CONCURRENCY = settings.DEBUG and 1 or 8
HASH_ALGORITHM = "sha1"
SENTRYCLI_SEMVER_RE = re.compile(r"^sentry-cli\/(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)")
API_PREFIX = "/api/0"
CHUNK_UPLOAD_ACCEPT = (
    "debug_files",  # DIF assemble
    "release_files",  # Release files assemble
    "pdbs",  # PDB upload and debug id override
    "sources",  # Source artifact bundle upload
    "bcsymbolmaps",  # BCSymbolMaps and associated PLists/UuidMaps
    "il2cpp",  # Il2cpp LineMappingJson files
    "portablepdbs",  # Portable PDB debug file
    "artifact_bundles",  # Artifact Bundles for JavaScript Source Maps
    "artifact_bundles_v2",  # The `assemble` endpoint will check for missing chunks
)


class GzipChunk(BytesIO):
    def __init__(self, file):
        data = GzipFile(fileobj=file, mode="rb").read()
        self.size = len(data)
        self.name = file.name
        super().__init__(data)


@region_silo_endpoint
class ChunkUploadEndpoint(OrganizationEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
        "POST": ApiPublishStatus.PRIVATE,
    }
    owner = ApiOwner.OWNERS_NATIVE
    permission_classes = (OrganizationReleasePermission,)
    rate_limits = RateLimitConfig(group="CLI")

    def get(self, request: Request, organization) -> Response:
        """
        Return chunk upload parameters
        ``````````````````````````````
        :auth: required
        """
        endpoint = options.get("system.upload-url-prefix")
        relative_url = reverse("sentry-api-0-chunk-upload", args=[organization.slug])

        # Starting `sentry-cli@1.70.1` we added a support for relative chunk-uploads urls
        # User-Agent: sentry-cli/1.70.1
        user_agent = request.headers.get("User-Agent", "")
        sentrycli_version = SENTRYCLI_SEMVER_RE.search(user_agent)
        sentrycli_version_split = None
        if sentrycli_version is not None:
            sentrycli_version_split = (
                int(sentrycli_version.group("major")),
                int(sentrycli_version.group("minor")),
                int(sentrycli_version.group("patch")),
            )

        relative_urls_disabled = options.get("hybrid_cloud.disable_relative_upload_urls")
        requires_region_url = sentrycli_version_split and sentrycli_version_split >= (2, 30, 0)

        supports_relative_url = (
            not relative_urls_disabled
            and not requires_region_url
            and sentrycli_version_split
            and sentrycli_version_split >= (1, 70, 1)
        )

        # If user do not overwritten upload url prefix
        if len(endpoint) == 0:
            # And we support relative url uploads, return a relative, versionless endpoint (with `/api/0` stripped)
            if supports_relative_url:
                url = relative_url.lstrip(API_PREFIX)
            # Otherwise, if we do not support them, return an absolute, versioned endpoint with a default, system-wide prefix
            else:
                # We need to generate region specific upload URLs when possible to avoid hitting the API proxy
                # which tends to cause timeouts and performance issues for uploads.
                url = absolute_uri(relative_url, generate_region_url())
        else:
            # If user overridden upload url prefix, we want an absolute, versioned endpoint, with user-configured prefix
            url = absolute_uri(relative_url, endpoint)

        accept = CHUNK_UPLOAD_ACCEPT

        return Response(
            {
                "url": url,
                "chunkSize": settings.SENTRY_CHUNK_UPLOAD_BLOB_SIZE,
                "chunksPerRequest": MAX_CHUNKS_PER_REQUEST,
                "maxFileSize": get_max_file_size(organization),
                "maxRequestSize": MAX_REQUEST_SIZE,
                "concurrency": MAX_CONCURRENCY,
                "hashAlgorithm": HASH_ALGORITHM,
                "compression": ["gzip"],
                "accept": accept,
            }
        )

    def post(self, request: Request, organization) -> Response:
        """
        Upload chunks and store them as FileBlobs
        `````````````````````````````````````````
        :pparam file file: The filename should be sha1 hash of the content.
                            Also not you can add up to MAX_CHUNKS_PER_REQUEST files
                            in this request.

        :auth: required
        """
        # Create a unique instance so our logger can be decoupled from the request
        # and used in threads.
        logger = logging.getLogger("sentry.files")
        logger.info("chunkupload.start")

        files = []
        if request.data:
            files = request.data.getlist("file")
            files += [GzipChunk(chunk) for chunk in request.data.getlist("file_gzip")]

        if len(files) == 0:
            # No files uploaded is ok
            logger.info("chunkupload.end", extra={"status": status.HTTP_200_OK})
            return Response(status=status.HTTP_200_OK)

        logger.info("chunkupload.post.files", extra={"len": len(files)})

        # Validate file size
        checksums = []
        size = 0
        for chunk in files:
            size += chunk.size
            if chunk.size > settings.SENTRY_CHUNK_UPLOAD_BLOB_SIZE:
                logger.info("chunkupload.end", extra={"status": status.HTTP_400_BAD_REQUEST})
                return Response(
                    {"error": "Chunk size too large"}, status=status.HTTP_400_BAD_REQUEST
                )
            checksums.append(chunk.name)

        if size > MAX_REQUEST_SIZE:
            logger.info("chunkupload.end", extra={"status": status.HTTP_400_BAD_REQUEST})
            return Response({"error": "Request too large"}, status=status.HTTP_400_BAD_REQUEST)

        if len(files) > MAX_CHUNKS_PER_REQUEST:
            logger.info("chunkupload.end", extra={"status": status.HTTP_400_BAD_REQUEST})
            return Response({"error": "Too many chunks"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            FileBlob.from_files(zip(files, checksums), organization=organization, logger=logger)
        except OSError as err:
            logger.info("chunkupload.end", extra={"status": status.HTTP_400_BAD_REQUEST})
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("chunkupload.end", extra={"status": status.HTTP_200_OK})
        return Response(status=status.HTTP_200_OK)


# chunking-test-giant-1775917279-27

def _gen_1775917279_27_0(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 0 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_1(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 1 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_2(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 2 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_3(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 3 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_4(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 4 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_5(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 5 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_6(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 6 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_7(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 7 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_8(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 8 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_9(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 9 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_10(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 10 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_11(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 11 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_12(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 12 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_13(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 13 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_14(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 14 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_15(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 15 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_16(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 16 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_17(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 17 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_18(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 18 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_19(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 19 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_20(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 20 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_21(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 21 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_22(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 22 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_23(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 23 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_24(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 24 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_25(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 25 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_26(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 26 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_27(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 27 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_28(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 28 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_29(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 29 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_30(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 30 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_31(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 31 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_32(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 32 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_33(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 33 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_34(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 34 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_35(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 35 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_36(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 36 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_37(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 37 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_38(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 38 + y - z
    return result if result > 0 else None

def _gen_1775917279_27_39(x, y, z):
    """Auto-generated."""
    if x is None: return None
    result = x * 39 + y - z
    return result if result > 0 else None

