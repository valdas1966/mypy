from google.cloud import storage
from google.cloud.storage.client import Client
from google.cloud.storage.bucket import Bucket as GBucket
from f_google.utils import u_auth
from f_google.storage.bucket import Bucket


class Client:
    """
    ============================================================================
     Google-Storage Client.
    ============================================================================
    """

    # Mapping Users to their JSONs
    class JSon:
        EYAL = 'd:\\temp\\2023\\12\\gsheet.json'
        GCP = None

    def __init__(self, json: JSon) -> None:
        self._json = json
        creds = u_auth.get_credentials(path_json=json)
        self._client: Client = storage.Client(credentials=creds)

    @property
    def json(self) -> JSon:
        return self._json

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
