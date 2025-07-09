from f_google import Auth, ServiceAccount
from .main import Storage


class Factory:
    """
    ============================================================================
     Factory for Google-Cloud-Storage.
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
