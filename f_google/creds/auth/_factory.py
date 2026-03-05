from google.oauth2.service_account import Credentials as SACredentials
from f_google.creds.auth.main import Auth
from pathlib import Path
from os import environ
import sys


class Factory:
    """
    ============================================================================
     Factory for Google Service-Account Authentication.
    ============================================================================
    """

    _SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
               'https://www.googleapis.com/auth/drive',
               'https://www.googleapis.com/auth/spreadsheets',
               'https://www.googleapis.com/auth/presentations']

    @staticmethod
    def rami() -> SACredentials:
        """
        ====================================================================
         Return Service-Account Credentials for RAMI (project: noteret).
        ====================================================================
        """
        if sys.platform == 'darwin':
            path = str(Path.home() / 'prof' / 'rami.json')
        else:
            path = environ['RAMI_JSON_PATH']
        return Auth.get_creds(path=path, scopes=Factory._SCOPES)
