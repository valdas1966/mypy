from f_core.mixins.has import HasName
from google.cloud.storage.blob import Blob as GBlob
from typing import Optional, Union, BinaryIO
from io import BytesIO


class Blob(HasName):
    """
    ============================================================================
     Wrapper for Google-Cloud-Storage BLOB (Binary Large Object).
    ============================================================================
    """

    def __init__(self, g_blob: GBlob) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=g_blob.name)
        self._g_blob = g_blob

    @property
    def size(self) -> Optional[int]:
        """
        ========================================================================
         Get blob size in bytes.
        ========================================================================
        """
        return self._g_blob.size

    @property
    def content_type(self) -> Optional[str]:
        """
        ========================================================================
         Get blob content type.
        ========================================================================
        """
        return self._g_blob.content_type

    @property
    def time_created(self):
        """
        ========================================================================
         Get blob creation time.
        ========================================================================
        """
        return self._g_blob.time_created

    @property
    def updated(self):
        """
        ========================================================================
         Get blob last updated time.
        ========================================================================
        """
        return self._g_blob.updated

    def exists(self) -> bool:
        """
        ========================================================================
         Check if blob exists in storage.
        ========================================================================
        """
        return self._g_blob.exists()

    def delete(self) -> bool:
        """
        ========================================================================
         Delete the blob from storage.
        ========================================================================
        """
        try:
            self._g_blob.delete()
            return True
        except Exception:
            return False

    def download_as_bytes(self) -> bytes:
        """
        ========================================================================
         Download blob content as bytes.
        ========================================================================
        """
        return self._g_blob.download_as_bytes()

    def download_as_text(self, encoding: str = 'utf-8') -> str:
        """
        ========================================================================
         Download blob content as text.
        ========================================================================
        """
        return self._g_blob.download_as_text(encoding=encoding)

    def download_to_filename(self, filename: str) -> bool:
        """
        ========================================================================
         Download blob to a local file.
        ========================================================================
        """
        try:
            self._g_blob.download_to_filename(filename)
            return True
        except Exception:
            return False

    def download_to_file(self, file_obj: BinaryIO) -> bool:
        """
        ========================================================================
         Download blob to a file-like object.
        ========================================================================
        """
        try:
            self._g_blob.download_to_file(file_obj)
            return True
        except Exception:
            return False

    def upload_from_filename(self, filename: str, content_type: Optional[str] = None) -> bool:
        """
        ========================================================================
         Upload blob from a local file.
        ========================================================================
        """
        try:
            self._g_blob.upload_from_filename(filename, content_type=content_type)
            return True
        except Exception:
            return False

    def upload_from_file(self, file_obj: BinaryIO, content_type: Optional[str] = None) -> bool:
        """
        ========================================================================
         Upload blob from a file-like object.
        ========================================================================
        """
        try:
            self._g_blob.upload_from_file(file_obj, content_type=content_type)
            return True
        except Exception:
            return False

    def upload_from_string(self, data: Union[str, bytes], content_type: Optional[str] = None) -> bool:
        """
        ========================================================================
         Upload blob from string or bytes.
        ========================================================================
        """
        try:
            self._g_blob.upload_from_string(data, content_type=content_type)
            return True
        except Exception:
            return False

    def make_public(self) -> bool:
        """
        ========================================================================
         Make blob publicly accessible.
        ========================================================================
        """
        try:
            self._g_blob.make_public()
            return True
        except Exception:
            return False

    def make_private(self) -> bool:
        """
        ========================================================================
         Make blob private.
        ========================================================================
        """
        try:
            self._g_blob.make_private()
            return True
        except Exception:
            return False

    def generate_signed_url(self, expiration, method: str = 'GET') -> str:
        """
        ========================================================================
         Generate a signed URL for the blob.
        ========================================================================
        """
        return self._g_blob.generate_signed_url(expiration=expiration, method=method)

    def reload(self) -> bool:
        """
        ========================================================================
         Reload blob properties from storage.
        ========================================================================
        """
        try:
            self._g_blob.reload()
            return True
        except Exception:
            return False

    def patch(self) -> bool:
        """
        ========================================================================
         Update blob properties.
        ========================================================================
        """
        try:
            self._g_blob.patch()
            return True
        except Exception:
            return False

    @property
    def public_url(self) -> str:
        """
        ========================================================================
         Get public URL for the blob.
        ========================================================================
        """
        return self._g_blob.public_url

    @property
    def media_link(self) -> Optional[str]:
        """
        ========================================================================
         Get media download link for the blob.
        ========================================================================
        """
        return self._g_blob.media_link
