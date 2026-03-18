from f_google.services.drive.main import Drive
from f_google.creds.oauth import OAuth


class Factory:
    """
    ========================================================================
     Factory for Google Drive Client.
    ========================================================================
    """

    @staticmethod
    def valdas() -> Drive:
        """
        ====================================================================
         Return a Drive Client with VALDAS OAuth Credentials.
        ====================================================================
        """
        creds = OAuth.Factory.valdas()
        return Drive(creds=creds)
