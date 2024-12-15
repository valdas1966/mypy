from googleapiclient.discovery import build, Resource
from f_google.utils.u_authentication import UAuthentication, Credentials


class UService:
    """
    ============================================================================
     Utils-Class for generating API for Google-Services.
    ============================================================================
    """

    @staticmethod
    def drive(user: str) -> Resource:
        """
        ========================================================================
         Return a Resource for interacting with Google-Drive API.
        ========================================================================
        """
        creds = UAuthentication.get(user=user)
        return UService._get_service(name='drive', version='v3', creds=creds)

    @staticmethod
    def sheets(user: str) -> Resource:
        """
        ========================================================================
         Return a Resource for interacting with Google-Sheets API.
        ========================================================================
        """
        creds = UAuthentication.get(user=user)
        return UService._get_service(name='sheets', version='v4', creds=creds)

    @staticmethod
    def _get_service(name: str,
                     version: str,
                     creds: Credentials
                     ) -> Resource:
        """
        ========================================================================
         Return a Resource for interacting with Google-API.
        ========================================================================
        """
        return build(serviceName=name,
                     version=version,
                     credentials=creds)
