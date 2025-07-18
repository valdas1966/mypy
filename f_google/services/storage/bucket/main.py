from f_google.services.storage.bucket.blob.main import Blob
from google.cloud.storage.bucket import Bucket as GBucket
from f_core.mixins.has.name import HasName
import requests
import tempfile
import os


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
        
    def names_blobs(self, prefix: str = None) -> list[str]:
        """
        ========================================================================
         Get names of all blobs in the bucket.
        ========================================================================
        """
        return [blob.name
                for blob
                in self._g_bucket.list_blobs(prefix=prefix)]

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
        return Blob(g_blob=g_blob)

    def upload_from_pc(self,
                       name: str,
                       path: str) -> bool:
        """
        ========================================================================
         Upload a file from the local machine to the bucket.
        ========================================================================
        """
        try:
            blob = self._g_bucket.blob(name)
            blob.upload_from_filename(path)
            return True
        except Exception:
            return False
    
    def upload_from_url(self,
                        name: str,
                        url: str) -> bool:
        """
        ========================================================================
         Upload a file from a URL to the bucket.
        ========================================================================
        """
        SIZE_LARGE = 100
        try:
            response = requests.head(url, allow_redirects=True)
            size_header = response.headers.get('Content-Length')
            size_mb = int(size_header) / 1_048_576 if size_header else SIZE_LARGE
            if size_mb < SIZE_LARGE:
                return self._upload_from_url_small(name, url)   
            else:
                return self._upload_from_url_large(name, url)
        except Exception:
            return False

    def _upload_from_url_small(self, 
                               name: str,
                               url: str) -> bool:
        """
        ========================================================================
         Upload a file from a URL to the bucket.
        ========================================================================
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            blob = self._g_bucket.blob(name)
            blob.upload_from_string(response.content)
            return True
        except Exception:
            return False
        
    def _upload_from_url_large(self, name: str, url: str) -> bool:
        """
        ========================================================================
         Stream download to a temp file, close it, upload, then delete.
        ========================================================================
        """
        tmp_path: str | None = None
        try:
            with requests.get(url, stream=True, timeout=60) as rsp:
                rsp.raise_for_status()
                # create temp file that we can reopen later
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_path = tmp_file.name
                    for chunk in rsp.iter_content(chunk_size=8192):
                        if chunk:
                            tmp_file.write(chunk)
            # file is **closed** here → safe to reopen on Windows
            blob = self._g_bucket.blob(name)
            blob.upload_from_filename(tmp_path)
            return True
        except Exception:
            return False
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
