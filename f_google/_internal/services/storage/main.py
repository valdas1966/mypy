from google.cloud import storage
from f_ds.mixins.collectionable import Collectionable
from f_google._internal.auth import ServiceAccount
from f_google._internal.services.storage.bucket import Bucket
from f_google._internal.services._base import BaseGoogleService

class Storage(BaseGoogleService, Collectionable):
    """
    ============================================================================
     Google Cloud Storage client wrapper with enhanced functionality.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 service_account: ServiceAccount) -> None:
        """
        ========================================================================
         Initialize Storage client with credentials.
        ========================================================================
        """
        BaseGoogleService.__init__(self,
                                   service_account=ServiceAccount.RAMI,
                                   is_valid=bool(self._client))
        self._client = storage.Client(credentials=creds)

    def buckets(self) -> list[Bucket]:
        """
        ========================================================================
         Get all buckets in the storage.
        ========================================================================
        """
        return [Bucket(bucket) for bucket in self._client.list_buckets()]

    def names_buckets(self) -> list[str]:
        """
        ========================================================================
         Get names of all buckets in the storage.
        ========================================================================
        """
        return [bucket.name for bucket in self._client.list_buckets()]  
    
    def to_iterable(self) -> list[Bucket]:
        """
        ========================================================================
         Return Iterable of Buckets.
        ========================================================================
        """
        return self.buckets()

    def __contains__(self, item: Bucket | str) -> bool:
        """
        ========================================================================
         Return True if the Storage contains a received Bucket.
        ========================================================================
        """
        if isinstance(item, Bucket):
            return item in self.buckets()
        elif isinstance(item, str):
            return item in self.names_buckets()
        else:
            raise TypeError

    def __getitem__(self, item: str) -> Bucket:
        """
        ========================================================================
         Get Bucket by Name.
        ========================================================================
        """

        return Bucket(g_bucket=self._client.get_bucket(item))
