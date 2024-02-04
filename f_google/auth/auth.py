from frozendict import frozendict
from google.oauth2.service_account import Credentials
import google.auth


class Auth:

    # Paths to JSon-Keys to Google Account
    _JSONS = frozendict({'VALDAS': 'd:\\temp\\2023\\12\\gsheet.json'})

    @staticmethod
    def get_creds(user: str = None) -> Credentials:
        """
        ========================================================================
         Return Google-Cloud Service Account Credentials from a JSON-File.
         If no User provided, return a current GCP creds (default).
        ========================================================================
        """
        if not user:
            return google.auth.default()[0]
        scopes = ['https://www.googleapis.com/auth/cloud-platform',
                  'https://www.googleapis.com/auth/spreadsheets']
        return Credentials.from_service_account_file(filename=Auth._JSONS[user],
                                                     scopes=scopes)
