from .main import Bucket
from google.cloud.storage.bucket import Bucket as GBucket
from google.cloud import storage
from f_google._internal.auth import Auth, ServiceAccount


class Factory:
    """
    ============================================================================
    Factory for Google Cloud Storage Bucket operations.
    ============================================================================
    """

    @staticmethod
    def from_name(bucket_name: str, account: ServiceAccount) -> Bucket:
        """
        ========================================================================
        Create Bucket instance from bucket name and service account.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        client = storage.Client(credentials=creds)
        g_bucket = client.bucket(bucket_name)
        return Bucket(g_bucket)

    @staticmethod
    def rami(bucket_name: str) -> Bucket:
        """
        ========================================================================
        Create Bucket instance with RAMI service account.
        ========================================================================
        """
        return Factory.from_name(bucket_name, ServiceAccount.RAMI)

    @staticmethod
    def valdas(bucket_name: str) -> Bucket:
        """
        ========================================================================
        Create Bucket instance with VALDAS service account.
        ========================================================================
        """
        return Factory.from_name(bucket_name, ServiceAccount.VALDAS)

    @staticmethod
    def from_g_bucket(g_bucket: GBucket) -> Bucket:
        """
        ========================================================================
        Create Bucket instance from existing Google Cloud Storage bucket.
        ========================================================================
        """
        return Bucket(g_bucket)