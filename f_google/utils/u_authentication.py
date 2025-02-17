from google.oauth2.service_account import Credentials
from f_google.user import User
import google.auth



class UAuthentication:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """

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
                  'https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/presentations']
        return Credentials.from_service_account_file(filename=user,
                                                     scopes=scopes)
