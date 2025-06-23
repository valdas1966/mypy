from google.cloud import storage
from f_google.google import Credentials


class Storage:

    def __init__(self, creds: Credentials) -> None:
        self._client = storage.Client(credentials=creds)

    def list_buckets(self) -> list[str]:
        """
        ============================================================================
        List all accessible bucket names for the current service account.
        ============================================================================
        """
        buckets = self._client.list_buckets()
        return [bucket.name for bucket in buckets]
