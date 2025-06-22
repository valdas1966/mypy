from google.oauth2.credentials import Credentials
from os import environ


class Auth:
    """
    ============================================================================
     Static-Methods for Google Authentication process.
    ============================================================================
    """

    @staticmethod
    def get(user: str = None) -> Credentials:
        """
        ========================================================================
        """
        if not user:
            return Credentials.from_authorized_user_file(filename=environ['GOOGLE_APPLICATION_CREDENTIALS'],
                                                         scopes=['https://www.googleapis.com/auth/cloud-platform',
                                                                 'https://www.googleapis.com/auth/drive',
                                                                 'https://www.googleapis.com/auth/spreadsheets',
                                                                 'https://www.googleapis.com/auth/presentations'])
        return Credentials.from_authorized_user_file(filename=user,
                                                     scopes=['https://www.googleapis.com/auth/cloud-platform',
                                                             'https://www.googleapis.com/auth/drive',