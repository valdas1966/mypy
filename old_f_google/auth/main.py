from google.oauth2.service_account import Credentials
from old_f_google.auth._enums import ServiceAccount
from f_psl.sys import utils
from pathlib import Path
from os import environ


class Auth:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """
    
    # Factory
    Factory: type = None

    # Path in Mac
    path_mac = Path.home() / 'prof' / 'rami.json'

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
        if utils.is_mac():
            path = Auth.path_mac
        else:
            var = f'{account.value}_JSON_PATH'
            path = environ[var]
        return Credentials.from_service_account_file(filename=path,
                                                     scopes=scopes)
