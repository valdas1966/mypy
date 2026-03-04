from f_google.sheets.main import Sheets
from f_google.oauth import OAuth


class Factory:
    """
    ============================================================================
     Factory for Google Sheets Client.
    ============================================================================
    """

    @staticmethod
    def valdas(id_spread: str) -> Sheets:
        """
        ====================================================================
         Return a Sheets Client for VALDAS OAuth Credentials.
        ====================================================================
        """
        creds = OAuth.Factory.valdas()
        return Sheets(creds=creds, id_spread=id_spread)
