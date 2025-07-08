from google.cloud import storage
from google.cloud.storage.bucket import Bucket as GBucket
from f_google._internal.auth import Credentials
from .bucket import Bucket
from typing import Optional


class Storage:
    """
    ============================================================================
    Google Cloud Storage client wrapper with enhanced functionality.
    ============================================================================
    """

    def __init__(self, creds: Credentials) -> None:
        """
        ========================================================================
        Initialize Storage client with credentials.
        ========================================================================
        """
        self._client = storage.Client(credentials=creds)

    def list_buckets(self) -> list[str]:
        """
        ============================================================================
        List all accessible bucket names for the current service account.
        ============================================================================
        """
        buckets = self._client.list_buckets()
        return [bucket.name for bucket in buckets]
    
    def create_bucket(self, name: str, location: str = 'US') -> Bucket:
        """
        ========================================================================
        Create a new bucket and return wrapped Bucket instance.
        ========================================================================
        """
        g_bucket = self._client.create_bucket(bucket_or_name=name, location=location)
        return Bucket(g_bucket)
    
    def delete_bucket(self, name: str, force: bool = False) -> None:
        """
        ========================================================================
        Delete a bucket. If force=True, deletes all objects first.
        ========================================================================
        """
        bucket = self._client.bucket(name)
        if force:
            bucket.delete(force=True)
        else:
            bucket.delete()
    
    def get_bucket(self, name: str) -> Bucket:
        """
        ========================================================================
        Get bucket by name and return wrapped Bucket instance.
        ========================================================================
        """
        g_bucket = self._client.bucket(name)
        return Bucket(g_bucket)
    
    def __getitem__(self, name: str) -> Bucket:
        """
        ========================================================================
        Get bucket by name using dictionary-style access: storage[bucket_name]
        ========================================================================
        """
        return self.get_bucket(name)
