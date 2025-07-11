from .main import Blob
from google.cloud.storage.blob import Blob as GBlob
from google.cloud import storage
from f_google._internal.auth import Auth, ServiceAccount


class Factory:
    """
    ============================================================================
     Factory for Google-Cloud-Storage Blob objects.
    ============================================================================
    """

    @staticmethod
    def from_pc(path_src: str, path_dst: str) -> Blob:
        """
        ========================================================================
         Create a Blob from a local file.
        ========================================================================
        """
        with open(path_src, 'rb') as f:
            gblob = GBlob(f.read(), bucket=path_dst)
            blob = Blob(g_blob=gblob)
            
        return blob
    