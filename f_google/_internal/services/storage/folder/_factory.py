from .main import Folder
from google.cloud import storage
from f_google._internal.auth import Auth, ServiceAccount


class Factory:
    """
    ============================================================================
    Factory for Google Cloud Storage Folder operations.
    ============================================================================
    """

    @staticmethod
    def from_path(bucket_name: str, folder_path: str, account: ServiceAccount) -> Folder:
        """
        ========================================================================
        Create Folder instance from bucket and folder path with service account.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        client = storage.Client(credentials=creds)
        bucket = client.bucket(bucket_name)
        return Folder(bucket, folder_path)

    @staticmethod
    def rami(bucket_name: str, folder_path: str = '') -> Folder:
        """
        ========================================================================
        Create Folder instance with RAMI service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, folder_path, ServiceAccount.RAMI)

    @staticmethod
    def valdas(bucket_name: str, folder_path: str = '') -> Folder:
        """
        ========================================================================
        Create Folder instance with VALDAS service account.
        ========================================================================
        """
        return Factory.from_path(bucket_name, folder_path, ServiceAccount.VALDAS)

    @staticmethod
    def root(bucket_name: str, account: ServiceAccount) -> Folder:
        """
        ========================================================================
        Create root folder instance (empty path).
        ========================================================================
        """
        return Factory.from_path(bucket_name, '', account)

    @staticmethod
    def root_rami(bucket_name: str) -> Folder:
        """
        ========================================================================
        Create root folder instance with RAMI service account.
        ========================================================================
        """
        return Factory.rami(bucket_name, '')

    @staticmethod
    def root_valdas(bucket_name: str) -> Folder:
        """
        ========================================================================
        Create root folder instance with VALDAS service account.
        ========================================================================
        """
        return Factory.valdas(bucket_name, '')