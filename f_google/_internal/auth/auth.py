from google.oauth2.service_account import Credentials
from ._internal.service_account import ServiceAccount
from os import environ


class Auth:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """
    
    Factory: type = None

    _SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
               'https://www.googleapis.com/auth/drive',
               'https://www.googleapis.com/auth/spreadsheets',
               'https://www.googleapis.com/auth/presentations']
               
    @staticmethod
    def get_creds(account: ServiceAccount) -> Credentials:
        """
        ========================================================================
         Returns the credentials for the given service account.
        ========================================================================
        """
        scopes = Auth._SCOPES
        var = f'{account.value}_JSON_PATH'
        path = environ[var]
        return Credentials.from_service_account_file(filename=path,
                                                     scopes=scopes)
