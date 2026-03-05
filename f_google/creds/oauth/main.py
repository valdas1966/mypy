from google.oauth2.credentials import Credentials as OAuthCredentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path


class OAuth:
    """
    ============================================================================
     Static-Methods for Google OAuth Authentication.
    ============================================================================
    """

    # Factory
    Factory: type = None

    @staticmethod
    def get_creds(path_client: str,
                  path_token: str,
                  scopes: list[str]) -> OAuthCredentials:
        """
        ====================================================================
         Return OAuth Credentials.
         Opens browser for login on first use, caches token after.
        ====================================================================
        """
        creds = None
        # Load cached token
        if Path(path_token).exists():
            creds = OAuthCredentials.from_authorized_user_file(
                filename=path_token,
                scopes=scopes
            )
        # Refresh or re-authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=path_client,
                    scopes=scopes
                )
                creds = flow.run_local_server(port=0)
            # Cache token
            with open(path_token, 'w') as f:
                f.write(creds.to_json())
        return creds
