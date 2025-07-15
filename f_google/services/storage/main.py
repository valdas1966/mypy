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
        self._is_valid = bool(self._client)
        
    def buckets(self) -> list[Bucket]:
        """
        ========================================================================
         Get all buckets in the storage.
        ========================================================================
        """
        return [Bucket(g_bucket=g_bucket)
                for g_bucket
                in self._client.list_buckets()]
        
    def names_buckets(self) -> list[str]:
        """
        ========================================================================
         Get all bucket names.
        ========================================================================
        """
        return [bucket.name for bucket in self.buckets()]
    
    def bucket(self, name: str) -> Bucket | None:
        """
        ========================================================================
         Get a bucket by name.
        ========================================================================
        """
        if name in self.names_buckets():
            return Bucket(g_bucket=self._client.bucket(name))
        return None
