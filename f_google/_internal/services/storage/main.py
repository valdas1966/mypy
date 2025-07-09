from google.cloud import storage
from f_core.mixins.validatable import Validatable
from f_google.google import Credentials


class Storage(Validatable):
    """
    ============================================================================
     Google Cloud Storage client wrapper with enhanced functionality.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, creds: Credentials) -> None:
        """
        ========================================================================
         Initialize Storage client with credentials.
        ========================================================================
        """
        self._client = storage.Client(credentials=creds)
        Validatable.__init__(self, is_valid=bool(self._client))

    def names_buckets(self) -> list[str]:
        """
        ========================================================================
         Get names of all buckets in the storage.
        ========================================================================
        """
        return [bucket.name for bucket in self._client.list_buckets()]  


    