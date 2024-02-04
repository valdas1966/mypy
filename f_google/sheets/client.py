import gspread
from f_google.client.base import ClientBase
from f_google.sheets.spread import Spread


class Client(ClientBase):
    """
    ============================================================================
     Google-Sheets Client.
    ============================================================================
    """

    def open_spread(self, id_spread: str) -> Spread:
        """
        ========================================================================
         Return a Spreadsheet Class by its ID.
        ========================================================================
        """
        spread: gspread.spreadsheet = self._client.open_by_key(key=id_spread)
        return Spread(id_spread=id_spread, spread=spread)

    def _open_client(self) -> gspread.client.Client:
        """
        ========================================================================
         Open Google-Sheets Client.
        ========================================================================
        """
        return gspread.authorize(credentials=self.creds)