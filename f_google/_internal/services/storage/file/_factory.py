from .main import File
from google.cloud import storage
from f_google._internal.auth import Auth, ServiceAccount


class Factory:
    """
    ============================================================================
    Factory for Google Cloud Storage File operations.
    ============================================================================
    """

    @staticmethod
    def from_path(bucket_name: str, file_path: str, account: ServiceAccount) -> File:
        """
        ========================================================================
        Create File instance from bucket and file path with service account.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        client = storage.Client(credentials=creds)
        bucket = client.bucket(bucket_name)
        return File(bucket, file_path)

    @staticmethod
    def rami(bucket_name: str, file_path: str) -> File:
        """
        ========================================================================
        Create File instance with RAMI service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, file_path, ServiceAccount.RAMI)

    @staticmethod
    def valdas(bucket_name: str, file_path: str) -> File:
        """
        ========================================================================
        Create File instance with VALDAS service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, file_path, ServiceAccount.VALDAS)

    @staticmethod
    def create_new(bucket_name: str, file_path: str, account: ServiceAccount) -> File:
        """
        ========================================================================
        Create a new file instance ready for content upload.
        ========================================================================
        """
        return Factory.from_path(bucket_name, file_path, account)

    @staticmethod
    def create_new_rami(bucket_name: str, file_path: str) -> File:
        """
        ========================================================================
        Create a new file instance with RAMI service account.
        ========================================================================
        """
        return Factory.rami(bucket_name, file_path)

    @staticmethod
    def create_new_valdas(bucket_name: str, file_path: str) -> File:
        """
        ========================================================================
        Create a new file instance with VALDAS service account.
        ========================================================================
        """
        return Factory.valdas(bucket_name, file_path)