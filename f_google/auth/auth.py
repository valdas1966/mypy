from frozendict import frozendict
from google.oauth2.service_account import Credentials
import google.auth
import os


class Auth:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """

    # Paths to JSon-Keys to Google Account
    _JSONS = frozendict({'VALDAS': 'VALDAS',
                         #'RAMI': 'd:\\professor\\gcp\\owner.json'})
                         'RAMI': 'd:\\professor\\json\\viewer.json',
                         'GFUNC': 'd:\\professor\\json\\gfunc.json'})

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
        filename = os.environ.get(Auth._JSONS[user])
        return Credentials.from_service_account_file(filename=filename,
                                                     scopes=scopes)
