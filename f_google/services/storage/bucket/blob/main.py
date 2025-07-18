from google.cloud.storage.blob import Blob as GBlob
from f_core.mixins.has import HasName


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
    def size(self) -> int:
        """
        ========================================================================
         Get blob size in Megabytes.
        ========================================================================
        """
        _BYTES_IN_MIB = 1_048_576
        return int(self._g_blob.size / _BYTES_IN_MIB)
