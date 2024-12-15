from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from f_google.services.sheets.sheet import Sheet


class Spread:
    """
    ============================================================================
     Google-Sheets SpreadSheet.
     ID-SPREAD should be shared to client_email in GSHEET-JSON KEYS FILE.
    ============================================================================
    """

    def __init__(self, id_spread: str, spread: Spreadsheet) -> None:
        self._id_spread = id_spread
        self._spread = spread

    @property
    def id_spread(self) -> str:
        return self._id_spread

    def titles(self) -> list[str]:
        """
        ========================================================================
         Return List of Sheet's Titles in the SpreadSheet.
        ========================================================================
        """
        return [sheet.title for sheet in self._spread.worksheets()]

    def __getitem__(self, key: int | str) -> Sheet:
        """
        ========================================================================
         Get list Worksheet by its Name (str) or Index (int).
        ========================================================================
        """
        ws: Worksheet | None = None
        if isinstance(key, int):
            # Access by index
            ws = self._spread.get_worksheet(key)
        elif isinstance(key, str):
            # Access by name
            ws = self._spread.worksheet(key)
        return Sheet(ws=ws)
