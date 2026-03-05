import gspread
from f_google.services.sheets.row.main import Row


class Sheet:
    """
    ============================================================================
     Google Sheets Worksheet.
    ============================================================================
    """

    def __init__(self, ws: gspread.Worksheet) -> None:
        """
        ====================================================================
         Init with a gspread Worksheet.
        ====================================================================
        """
        self._ws = ws
        self._rows: list[Row] | None = None

    @property
    def name(self) -> str:
        """
        ====================================================================
         Return the Worksheet Name.
        ====================================================================
        """
        return self._ws.title

    def _load(self) -> None:
        """
        ====================================================================
         Lazy-load all values from the Worksheet.
        ====================================================================
        """
        if self._rows is None:
            values = self._ws.get_all_values()
            self._rows = [Row(values=row) for row in values]

    def __getitem__(self, row: int) -> Row:
        """
        ====================================================================
         Return a Row by Index (0-based).
        ====================================================================
        """
        self._load()
        return self._rows[row]

    def __len__(self) -> int:
        """
        ====================================================================
         Return the number of Rows.
        ====================================================================
        """
        self._load()
        return len(self._rows)
