from google.oauth2.service_account import Credentials as SACredentials
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from f_google.auth._enums import Account, TypeAuth
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
    def _get_dir() -> Path:
        """
        ====================================================================
         Return the directory for credential files.
         Mac: ~/prof/
         Windows: uses env vars (handled per method).
        ====================================================================
        """
        return Path.home() / 'prof'

    @staticmethod
    def _get_path_service_account(account: Account) -> str:
        """
        ====================================================================
         Return path to JSON key file for a Service Account.
         Mac: ~/prof/{account}.json
         Windows: {ACCOUNT}_JSON_PATH env var.
        ====================================================================
        """
        if sys.platform == 'darwin':
            return str(Auth._get_dir() / f'{account.account.lower()}.json')
        var = f'{account.account}_JSON_PATH'
        return environ[var]

    @staticmethod
    def _get_path_oauth_client() -> str:
        """
        ====================================================================
         Return path to OAuth client secrets JSON file.
         Mac: ~/prof/oauth_client.json
        ====================================================================
        """
        if sys.platform == 'darwin':
            return str(Auth._get_dir() / 'oauth_client.json')
        return environ['OAUTH_CLIENT_JSON_PATH']

    @staticmethod
    def _get_path_oauth_token(account: Account) -> str:
        """
        ====================================================================
         Return path to cached OAuth token for the given Account.
         Mac: ~/prof/{account}_token.json
        ====================================================================
        """
        name = account.account.lower()
        if sys.platform == 'darwin':
            return str(Auth._get_dir() / f'{name}_token.json')
        return environ[f'{account.account}_TOKEN_PATH']

    @staticmethod
    def _get_creds_service_account(account: Account) -> SACredentials:
        """
        ====================================================================
         Return Credentials for a Service Account.
        ====================================================================
        """
        path = Auth._get_path_service_account(account=account)
        return SACredentials.from_service_account_file(
            filename=path,
            scopes=Auth._SCOPES
        )

    @staticmethod
    def _get_creds_oauth(account: Account) -> OAuthCredentials:
        """
        ====================================================================
         Return OAuth Credentials for the given Account.
         Opens browser for login on first use, caches token after.
        ====================================================================
        """
        token_path = Auth._get_path_oauth_token(account=account)
        client_path = Auth._get_path_oauth_client()
        creds = None
        # Load cached token
        if Path(token_path).exists():
            creds = OAuthCredentials.from_authorized_user_file(
                filename=token_path,
                scopes=Auth._SCOPES
            )
        # Refresh or re-authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=client_path,
                    scopes=Auth._SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Cache token
            with open(token_path, 'w') as f:
                f.write(creds.to_json())
        return creds

    @staticmethod
    def get_creds(account: Account) -> Credentials:
        """
        ====================================================================
         Return Credentials for the given Account.
         Dispatches to Service-Account or OAuth based on Account type.
        ====================================================================
        """
        if account.type_auth == TypeAuth.SERVICE_ACCOUNT:
            return Auth._get_creds_service_account(account=account)
        return Auth._get_creds_oauth(account=account)
