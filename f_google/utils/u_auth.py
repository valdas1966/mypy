from google.oauth2.service_account import Credentials
import google.auth


def get_credentials(path_json: str = None) -> Credentials:
    """
    ============================================================================
     Return Google-Cloud Service Account Credentials from list JSON-File.
    ============================================================================
    """
    if not path_json:
        return google.auth.default()[0]
    scopes = ['https://www.googleapis.com/auth/cloud-platform',
              'https://www.googleapis.com/auth/spreadsheets']
    return Credentials.from_service_account_file(filename=path_json,
                                                 scopes=scopes)
