from google.oauth2.service_account import Credentials
from f_google.auth._enums import ServiceAccount
from pathlib import Path
from os import environ
import sys


class Auth:
    """
    ============================================================================
     Static-Methods for Google Authentication.
    ============================================================================
    """

    # Factory
    Factory: type = None

    _SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
               'https://www.googleapis.com/auth/drive',
               'https://www.googleapis.com/auth/spreadsheets',
               'https://www.googleapis.com/auth/presentations']

    @staticmethod
    def _get_path(account: ServiceAccount) -> str:
        """
        ========================================================================
         Return the path to the JSON key file for the given Service Account.
         Mac: ~/prof/{account}.json
         Windows: {ACCOUNT}_JSON_PATH env var.
        ========================================================================
        """
        if sys.platform == 'darwin':
            return str(Path.home() / 'prof' / f'{account.value.lower()}.json')
        var = f'{account.value}_JSON_PATH'
        return environ[var]

    @staticmethod
    def get_creds(account: ServiceAccount) -> Credentials:
        """
        ========================================================================
         Return Credentials for the given Service Account.
        ========================================================================
        """
        path = Auth._get_path(account=account)
        return Credentials.from_service_account_file(filename=path,
                                                     scopes=Auth._SCOPES)
