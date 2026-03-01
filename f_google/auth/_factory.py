from google.oauth2.service_account import Credentials
from f_google.auth.main import Auth
from f_google.auth._enums import ServiceAccount


class Factory:
    """
    ============================================================================
     Factory for Google Authentication.
    ============================================================================
    """

    @staticmethod
    def rami() -> Credentials:
        """
        ========================================================================
         Return Credentials for the RAMI Service Account.
        ========================================================================
        """
        return Auth.get_creds(account=ServiceAccount.RAMI)

    @staticmethod
    def valdas() -> Credentials:
        """
        ========================================================================
         Return Credentials for the VALDAS Service Account.
        ========================================================================
        """
        return Auth.get_creds(account=ServiceAccount.VALDAS)
