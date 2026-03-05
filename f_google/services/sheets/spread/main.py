from __future__ import annotations
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.oauth2.service_account import Credentials as SACredentials
from f_google.services.sheets.sheet import Sheet
from f_core.mixins.has import HasName
import gspread


class Spread(HasName):
    """
    ============================================================================
     Google Spreadsheet.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 creds: OAuthCredentials | SACredentials,
                 id_spread: str) -> None:
        """
        ====================================================================
         Init Google Spreadsheet Client and open by ID.
        ====================================================================
        """
        client: gspread.Client = gspread.authorize(creds)
        self._spread: gspread.Spreadsheet = client.open_by_key(id_spread)
        HasName.__init__(self, name=self._spread.title)

    @property
    def sheets(self) -> list[Sheet]:
        """
        ====================================================================
         Return all Worksheets as Sheet objects.
        ====================================================================
        """
        return [Sheet(ws=ws) for ws in self._spread.worksheets()]

    def __getitem__(self, name: str) -> Sheet:
        """
        ====================================================================
         Return a Sheet by Name.
        ====================================================================
        """
        return Sheet(ws=self._spread.worksheet(name))
