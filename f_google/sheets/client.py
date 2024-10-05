import gspread
from f_google.client.base import ClientBase
from f_google.sheets.spread import Spread


class GSheets(ClientBase):
    """
    ============================================================================
     Google-Sheets Client.
    ============================================================================
    """

    def open_spread(self, id_spread: str) -> Spread:
        """
        ========================================================================
         Return list Spreadsheet Class by its ID.
        ========================================================================
        """
        spread: gspread.spreadsheet = self._client.open_by_key(key=id_spread)
        return Spread(id_spread=id_spread, spread=spread)

    def _get_client(self) -> gspread.client.Client:
        """
        ========================================================================
         Open Google-Sheets Client.
        ========================================================================
        """
        return gspread.authorize(credentials=self.creds)
