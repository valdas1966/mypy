from f_core.mixins.has import HasName
from google.cloud.storage.blob import Blob as GBlob


class Blob(HasName):
    """
    ============================================================================
     Wrapper for Google-Cloud-Storage BLOB (Binary Large Object).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, blob: GBlob) -> None:
        """
        ========================================================================
        Initialize Blob wrapper with Google-Cloud-Storage blob instance.
        ========================================================================
        """
        HasName.__init__(self, name=blob.name)
        self._blob = blob

    @property
    def size(self) -> int:
        """
        ========================================================================
         Get blob size in bytes.
        ========================================================================
        """
        return self._blob.size

    def exists(self) -> bool:
        """
        ========================================================================
         Check if blob exists in the bucket.
        ========================================================================
        """
        return self._blob.exists()

    def delete(self) -> None:
        """
        ========================================================================
         Delete the blob from storage.
        ========================================================================
        """
        self._blob.delete()

    def download(self, path: str) -> None:
        """
        ========================================================================
         Download blob content to a local file.
        ========================================================================
        """
        with open(path, 'wb') as file:
            self._blob.download_to_file(file)

    def upload_from_file(self, file_path: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload content from a local file.
        ========================================================================
        """
        with open(file_path, 'rb') as file_obj:
            self._blob.upload_from_file(file_obj)
