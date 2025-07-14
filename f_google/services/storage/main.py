from google.cloud import storage
from f_ds.mixins.collectionable import Collectionable
from f_google.auth import ServiceAccount
from f_google.services.storage.bucket import Bucket
from f_google.services._base import BaseGoogleService


class Storage(BaseGoogleService, Collectionable):
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

    def __contains__(self, item: str) -> bool:
        """
        ========================================================================
         Return True if the Storage contains a received Bucket's Name.
        ========================================================================
        """
        return item in self.names_buckets()

    def __getitem__(self, item: str) -> Bucket:
        """
        ========================================================================
         Get Bucket by Name.
        ========================================================================
        """

        return Bucket(g_bucket=self._client.get_bucket(item))


storage = Storage()
bucket = storage['noteret_mp4']
print(bucket[0].name)
