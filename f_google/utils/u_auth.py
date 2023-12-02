from google.oauth2.service_account import Credentials


def get_credentials(path_json: str) -> Credentials:
    """
    ============================================================================
     Return Google-Cloud Service Account Credentials from a JSON-File.
    ============================================================================
    """
    scopes = ['https://www.googleapis.com/auth/cloud-platform',
              'https://www.googleapis.com/auth/spreadsheets']
    return Credentials.from_service_account_file(filename=path_json,
                                                 scopes=scopes)
