from google.cloud import storage
from f_google.auth import ServiceAccount
from f_google.services.storage.bucket import Bucket
from f_google.services._base import BaseGoogleService


class Storage(BaseGoogleService):
    """
    ============================================================================
     Google-Cloud-Storage Client Wrapper.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 service_account: ServiceAccount = ServiceAccount.RAMI) -> None:
        """
        ========================================================================
         Initialize Storage client with credentials.
        ========================================================================
        """
        BaseGoogleService.__init__(self, service_account=service_account)
        self._client = storage.Client(credentials=self._creds)
        
    def names_buckets(self) -> list[str]:
        """
        ========================================================================
         Get all bucket names.
        ========================================================================
        """
        return [bucket.name for bucket in self._client.list_buckets()]
    
    def create_bucket(self, name: str) -> Bucket:
        """
        ========================================================================
         Create a bucket by name.
        ========================================================================
        """
        g_bucket = self._client.create_bucket(name)
        return Bucket(g_bucket=g_bucket)

    def delete_bucket(self, name: str) -> bool:
        """
        ========================================================================
         Delete a bucket by name.
        ========================================================================
        """
        try:
            bucket = self._client.bucket(name)
            bucket.delete()
            return True
        except Exception:
            return False
        
    def get_bucket(self, name: str) -> Bucket:
        """
        ========================================================================
         Get a bucket by name.
        ========================================================================
        """
        try:
            g_bucket = self._client.get_bucket(name)
            return Bucket(g_bucket=g_bucket)
        except Exception:
            return None
