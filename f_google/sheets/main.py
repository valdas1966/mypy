from google.oauth2.credentials import Credentials as OAuthCredentials
import gspread


class Sheets:
    """
    ============================================================================
     Google Sheets Client.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 creds: OAuthCredentials,
                 id_spread: str) -> None:
        """
        ====================================================================
         Init Google Sheets Client and open a Spreadsheet by ID.
        ====================================================================
        """
        client = gspread.authorize(creds)
        self._spread = client.open_by_key(id_spread)

    @property
    def name(self) -> str:
        """
        ====================================================================
         Return the Spreadsheet name.
        ====================================================================
        """
        return self._spread.title

    @property
    def sheet_names(self) -> list[str]:
        """
        ====================================================================
         Return a list of Worksheet names.
        ====================================================================
        """
        return [ws.title for ws in self._spread.worksheets()]
