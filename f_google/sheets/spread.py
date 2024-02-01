from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from f_google.sheets.sheet import Sheet


class Spread:
    """
    ============================================================================
     Google-Sheets SpreadSheet.
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
         Get a Worksheet by its Name (str) or Index (int).
        ========================================================================
        """
        if isinstance(key, int):
            # Access by index
            ws: Worksheet = self._spread.get_worksheet(key)
        elif isinstance(key, str):
            # Access by name
            ws: Worksheet = self._spread.worksheet(key)
        return Sheet(ws=ws)
