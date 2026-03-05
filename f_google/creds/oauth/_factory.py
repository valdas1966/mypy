from google.oauth2.credentials import Credentials as OAuthCredentials
from f_google.creds.oauth.main import OAuth
from pathlib import Path
from os import environ
import sys


class Factory:
    """
    ============================================================================
     Factory for Google OAuth Authentication.
    ============================================================================
    """

    _SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
               'https://www.googleapis.com/auth/drive',
               'https://www.googleapis.com/auth/spreadsheets',
               'https://www.googleapis.com/auth/presentations']

    @staticmethod
    def valdas() -> OAuthCredentials:
        """
        ====================================================================
         Return OAuth Credentials for VALDAS.
        ====================================================================
        """
        if sys.platform == 'darwin':
            d = Path.home() / 'prof' / 'valdas'
            path_client = str(d / 'oauth_client.json')
            path_token = str(d / 'token.json')
        else:
            path_client = environ['OAUTH_CLIENT_JSON_PATH']
            path_token = environ['VALDAS_TOKEN_PATH']
        return OAuth.get_creds(path_client=path_client,
                               path_token=path_token,
                               scopes=Factory._SCOPES)
