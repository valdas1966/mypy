from google.auth.credentials import Credentials
from f_google.auth.main import Auth
from f_google.auth._enums import Account


class Factory:
    """
    ============================================================================
     Factory for Google Authentication.
    ============================================================================
    """

    @staticmethod
    def rami() -> Credentials:
        """
        ====================================================================
         Return Credentials for the RAMI Account (Service Account).
        ====================================================================
        """
        return Auth.get_creds(account=Account.RAMI)

    @staticmethod
    def valdas() -> Credentials:
        """
        ====================================================================
         Return Credentials for the VALDAS Account (OAuth).
        ====================================================================
        """
        return Auth.get_creds(account=Account.VALDAS)
