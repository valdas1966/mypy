from f_google.services.storage.bucket.blob.main import Blob
from google.cloud.storage.bucket import Bucket as GBucket
from f_core.mixins.has.name import HasName
import requests
from typing import Optional


class Bucket(HasName):
    """
    ============================================================================
     Wrapper for Google-Cloud-Storage Bucket.
    ============================================================================
    """

    def __init__(self, g_bucket: GBucket) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=g_bucket.name)
        self._g_bucket = g_bucket
        

    def list_blobs(self, prefix: Optional[str] = None) -> list[Blob]:
        """
        ========================================================================
         Get all Blobs in the Bucket.
        ========================================================================
        """
        return [Blob(g_blob=g_blob)
                for g_blob
                in self._g_bucket.list_blobs(prefix=prefix)]
        
    def blob_names(self, prefix: Optional[str] = None) -> list[str]:
        """
        ========================================================================
         Get names of all blobs in the bucket.
        ========================================================================
        """
        return [blob.name for blob in self._g_bucket.list_blobs(prefix=prefix)]

    def delete_blob(self, name: str) -> bool:
        """
        ========================================================================
         Delete a blob by name.
        ========================================================================
        """
        try:
            self._g_bucket.delete_blob(name)
            return True
        except Exception:
            return False
        
    def get_blob(self, name: str) -> Blob:
        """
        ========================================================================
         Get a blob by name.
        ========================================================================
        """
        g_blob = self._g_bucket.get_blob(name)
        if g_blob is None:
            g_blob = self._g_bucket.blob(name)
        return Blob(g_blob=g_blob)

    def blob(self, name: str) -> Blob:
        """
        ========================================================================
         Create a blob object (doesn't check if it exists).
        ========================================================================
        """
        return Blob(g_blob=self._g_bucket.blob(name))

    def upload_from_file(self, file_path: str, blob_name: str) -> bool:
        """
        ========================================================================
         Upload a file from the local machine to the bucket.
        ========================================================================
        """
        try:
            blob = self._g_bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            return True
        except Exception:
            return False
    
    def upload_from_url(self, url: str, blob_name: str) -> bool:
        """
        ========================================================================
         Upload a file from a URL to the bucket.
        ========================================================================
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            blob = self._g_bucket.blob(blob_name)
            blob.upload_from_string(response.content)
            return True
        except Exception:
            return False

    def download_to_file(self, blob_name: str, file_path: str) -> bool:
        """
        ========================================================================
         Download a blob to a local file.
        ========================================================================
        """
        try:
            blob = self._g_bucket.blob(blob_name)
            blob.download_to_filename(file_path)
            return True
        except Exception:
            return False

    def blob_exists(self, name: str) -> bool:
        """
        ========================================================================
         Check if a blob exists in the bucket.
        ========================================================================
        """
        try:
            blob = self._g_bucket.blob(name)
            return blob.exists()
        except Exception:
            return False
    
    def make_public(self) -> bool:
        """
        ========================================================================
         Make the bucket publicly readable.
        ========================================================================
        """
        try:
            self._g_bucket.make_public()
            return True
        except Exception:
            return False
    
    def make_private(self) -> bool:
        """
        ========================================================================
         Make the bucket private.
        ========================================================================
        """
        try:
            self._g_bucket.make_private()
            return True
        except Exception:
            return False    
    