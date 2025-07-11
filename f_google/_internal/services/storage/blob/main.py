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

    def __init__(self, g_blob: GBlob) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=g_blob.name)
        self._g_blob = g_blob

    @property
    def size(self) -> int:
        """
        ========================================================================
         Get g_blob size in bytes.
        ========================================================================
        """
        return self._g_blob.size

    def exists(self) -> bool:
        """
        ========================================================================
         Check if g_blob exists in the bucket.
        ========================================================================
        """
        return self._g_blob.exists()

    def delete(self) -> None:
        """
        ========================================================================
         Delete the g_blob from storage.
        ========================================================================
        """
        self._g_blob.delete()

    def download(self, path: str) -> None:
        """
        ========================================================================
         Download g_blob content to a local file.
        ========================================================================
        """
        with open(path, 'wb') as file:
            self._g_blob.download_to_file(file)
