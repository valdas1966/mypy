from f_google._internal.auth import Auth, ServiceAccount
from .main import Storage


class Factory:
    """
    ============================================================================
    Factory for Google Cloud Storage operations with common patterns.
    ============================================================================
    """

    @staticmethod
    def rami() -> Storage:
        """
        ========================================================================
        Get Storage instance authenticated with RAMI service account.
        ========================================================================
        """
        creds = Auth.get_creds(ServiceAccount.RAMI)
        return Storage(creds)

    @staticmethod
    def valdas() -> Storage:
        """
        ========================================================================
        Get Storage instance authenticated with VALDAS service account.
        ========================================================================
        """
        creds = Auth.get_creds(ServiceAccount.VALDAS)
        return Storage(creds)

    @staticmethod
    def from_account(account: ServiceAccount) -> Storage:
        """
        ========================================================================
        Get Storage instance authenticated with specified service account.
        ========================================================================
        """
        creds = Auth.get_creds(account)
        return Storage(creds)