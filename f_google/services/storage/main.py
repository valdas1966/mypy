from google.cloud import storage
from f_core.mixins.has.names import HasNames
from f_google.auth import ServiceAccount
from f_google.services.storage.bucket import Bucket
from f_google.services._base import BaseGoogleService


class Storage(BaseGoogleService, HasNames):
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
        HasNames.__init__(self, items=self._get_buckets())
        
    def _get_buckets(self) -> list[Bucket]:
        """
        ========================================================================
         Get all buckets in the storage.
        ========================================================================
        """
        return [Bucket(bucket) for bucket in self._client.list_buckets()]
