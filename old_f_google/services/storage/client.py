from google.cloud import storage
from google.cloud.storage.client import Client
from google.cloud.storage.bucket import Bucket as GBucket
from old_f_google.client.base import ClientBase
from old_f_google.services.storage.bucket import Bucket


class Storage(ClientBase):
    """
    ============================================================================
     Google-Storage Client.
    ============================================================================
    """

    def __init__(self, user: str) -> None:
        ClientBase.__init__(self, user=user)

    def bucket(self, name: str) -> Bucket:
        """
        ========================================================================
         Return Bucket by Name.
        ========================================================================
        """
        b: GBucket = self._client.bucket(bucket_name=name)
        return Bucket(bucket=b)

    def names_bucket(self) -> list[str]:
        """
        ========================================================================
         Return List of all Bucket-Names in the Client.
        ========================================================================
        """
        return [b.name for b in self._client.list_buckets()]

    def _get_client(self) -> Client:
        """
        ========================================================================
         Open and list Return list Storage-Client.
        ========================================================================
        """
        return storage.Client(credentials=self.creds)
