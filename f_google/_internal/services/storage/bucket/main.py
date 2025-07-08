from google.cloud.storage.bucket import Bucket as GBucket
from google.cloud.storage.blob import Blob as GBlob
from typing import Optional, List
import requests
from pathlib import Path
from ..blob import Blob
from ..folder import Folder
from ..file import File


class Bucket:
    """
    ============================================================================
    Google Cloud Storage bucket wrapper with enhanced blob operations.
    ============================================================================
    """

    def __init__(self, g_bucket: GBucket) -> None:
        """
        ========================================================================
        Initialize Bucket wrapper with Google Cloud Storage bucket instance.
        ========================================================================
        """
        self._bucket = g_bucket

    @property
    def name(self) -> str:
        """
        ========================================================================
        Get bucket name.
        ========================================================================
        """
        return self._bucket.name

    def list_blobs(self, prefix: Optional[str] = None) -> List[str]:
        """
        ========================================================================
        List all blob names in the bucket, optionally filtered by prefix.
        ========================================================================
        """
        blobs = self._bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def upload_file(self, local_path: str, blob_name: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload a file from local PC to the bucket.
        Args:
            local_path: Full path to local file
            blob_name: Name for the blob in bucket (defaults to filename)
        ========================================================================
        """
        if blob_name is None:
            blob_name = Path(local_path).name
        
        blob = self._bucket.blob(blob_name)
        with open(local_path, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

    def upload_from_url(self, url: str, blob_name: str) -> None:
        """
        ========================================================================
        Upload a file from URL directly to the bucket.
        Args:
            url: URL to download file from
            blob_name: Name for the blob in bucket
        ========================================================================
        """
        response = requests.get(url)
        response.raise_for_status()
        
        blob = self._bucket.blob(blob_name)
        blob.upload_from_string(response.content)

    def delete_blob(self, blob_name: str) -> None:
        """
        ========================================================================
        Delete a blob from the bucket.
        Args:
            blob_name: Name of the blob to delete
        ========================================================================
        """
        blob = self._bucket.blob(blob_name)
        blob.delete()

    def download_blob(self, blob_name: str, local_path: str) -> None:
        """
        ========================================================================
        Download a blob from the bucket to local PC.
        Args:
            blob_name: Name of the blob to download
            local_path: Local path where to save the file
        ========================================================================
        """
        blob = self._bucket.blob(blob_name)
        with open(local_path, 'wb') as file_obj:
            blob.download_to_file(file_obj)

    def blob_exists(self, blob_name: str) -> bool:
        """
        ========================================================================
        Check if a blob exists in the bucket.
        Args:
            blob_name: Name of the blob to check
        ========================================================================
        """
        blob = self._bucket.blob(blob_name)
        return blob.exists()

    def get_blob_size(self, blob_name: str) -> int:
        """
        ========================================================================
        Get the size of a blob in bytes.
        Args:
            blob_name: Name of the blob
        Returns:
            Size in bytes
        ========================================================================
        """
        blob = self._bucket.blob(blob_name)
        blob.reload()
        return blob.size

    def get_blob_url(self, blob_name: str) -> str:
        """
        ========================================================================
        Get public URL for a blob (if bucket allows public access).
        Args:
            blob_name: Name of the blob
        Returns:
            Public URL string
        ========================================================================
        """
        blob = self._bucket.blob(blob_name)
        return blob.public_url

    def __len__(self) -> int:
        """
        ========================================================================
        Get total number of blobs in the bucket.
        ========================================================================
        """
        return len(list(self._bucket.list_blobs()))

    def __contains__(self, blob_name: str) -> bool:
        """
        ========================================================================
        Check if blob exists using 'in' operator: 'file.txt' in bucket
        ========================================================================
        """
        return self.blob_exists(blob_name)

    # File System Abstraction Methods
    
    def get_blob(self, blob_name: str) -> Blob:
        """
        ========================================================================
        Get enhanced Blob wrapper for blob operations.
        ========================================================================
        """
        g_blob = self._bucket.blob(blob_name)
        return Blob(g_blob)

    def get_folder(self, folder_path: str = '') -> Folder:
        """
        ========================================================================
        Get Folder wrapper for folder operations.
        ========================================================================
        """
        return Folder(self._bucket, folder_path)

    def get_file(self, file_path: str) -> File:
        """
        ========================================================================
        Get File wrapper for file operations.
        ========================================================================
        """
        return File(self._bucket, file_path)

    def folder(self, folder_path: str = '') -> Folder:
        """
        ========================================================================
        Shorthand for get_folder().
        ========================================================================
        """
        return self.get_folder(folder_path)

    def file(self, file_path: str) -> File:
        """
        ========================================================================
        Shorthand for get_file().
        ========================================================================
        """
        return self.get_file(file_path)

    def blob(self, blob_name: str) -> Blob:
        """
        ========================================================================
        Shorthand for get_blob().
        ========================================================================
        """
        return self.get_blob(blob_name)

    @property
    def root(self) -> Folder:
        """
        ========================================================================
        Get root folder of the bucket.
        ========================================================================
        """
        return self.get_folder('')

    def walk(self):
        """
        ========================================================================
        Walk through all folders in the bucket.
        ========================================================================
        """
        return self.root.walk()

    def sync_from_local(self, local_folder_path: str, remote_folder_path: str = '', recursive: bool = True) -> None:
        """
        ========================================================================
        Sync local folder to bucket folder.
        ========================================================================
        """
        folder = self.get_folder(remote_folder_path)
        folder.sync_from_local(local_folder_path, recursive=recursive)

    def sync_to_local(self, local_folder_path: str, remote_folder_path: str = '', recursive: bool = True) -> None:
        """
        ========================================================================
        Sync bucket folder to local folder.
        ========================================================================
        """
        folder = self.get_folder(remote_folder_path)
        folder.sync_to_local(local_folder_path, recursive=recursive)