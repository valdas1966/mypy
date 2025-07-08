from .main import Blob
from google.cloud.storage.blob import Blob as GBlob
from google.cloud import storage
from f_google._internal.auth import Auth, ServiceAccount


class Factory:
    """
    ============================================================================
    Factory for Google Cloud Storage Blob operations.
    ============================================================================
    """

    @staticmethod
    def from_path(bucket_name: str, blob_name: str, account: ServiceAccount) -> Blob:
        """
        ========================================================================
        Create Blob instance from bucket and blob names with service account.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        client = storage.Client(credentials=creds)
        bucket = client.bucket(bucket_name)
        g_blob = bucket.blob(blob_name)
        return Blob(g_blob)

    @staticmethod
    def rami(bucket_name: str, blob_name: str) -> Blob:
        """
        ========================================================================
        Create Blob instance with RAMI service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, blob_name, ServiceAccount.RAMI)

    @staticmethod
    def valdas(bucket_name: str, blob_name: str) -> Blob:
        """
        ========================================================================
        Create Blob instance with VALDAS service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, blob_name, ServiceAccount.VALDAS)

    @staticmethod
    def from_g_blob(g_blob: GBlob) -> Blob:
        """
        ========================================================================
        Create Blob instance from existing Google Cloud Storage blob.
        ========================================================================
        """
        return Blob(g_blob)

    @staticmethod
    def create_new(bucket_name: str, blob_name: str, account: ServiceAccount) -> Blob:
        """
        ========================================================================
        Create a new blob instance ready for upload.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        client = storage.Client(credentials=creds)
        bucket = client.bucket(bucket_name)
        g_blob = bucket.blob(blob_name)
        return Blob(g_blob)