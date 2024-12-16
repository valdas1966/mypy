from frozendict import frozendict
from google.oauth2.service_account import Credentials
from f_utils import u_file
import google.auth
import os


class UAuthentication:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """

    # Paths to JSon-Keys to Google Account
    _JSONS = frozendict({'VALDAS': os.getenv(key='VALDAS_JSON_PATH'),
                         #'RAMI': 'd:\\professor\\gcp\\owner.json'})
                         'RAMI': 'd:\\professor\\json\\viewer.json',
                         'GFUNC': 'd:\\professor\\json\\gfunc.json'})

    @staticmethod
    def get(user: str = None) -> Credentials:
        """
        ========================================================================
         Return Google-Cloud Service Account Credentials from list JSON-File.
         If no User provided, return list current GCP creds (default).
        ========================================================================
        """
        if not user:
            return google.auth.default()[0]
        scopes = ['https://www.googleapis.com/auth/cloud-platform',
                  'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/spreadsheets']
        filename = UAuthentication._JSONS[user]
        # filename = u_file.to_drive(__file__) + filename[1:]
        return Credentials.from_service_account_file(filename=filename,
                                                     scopes=scopes)
