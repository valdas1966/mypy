from __future__ import annotations
import pandas as pd
from f_core.mixins.has.rows_cols import HasRowsCols


class Range(HasRowsCols):
    """
    ============================================================================
     2D Tabular Data Container (list of rows of string values).
    ============================================================================
    """

    def __init__(self, data: list[list[str]]) -> None:
        """
        ====================================================================
         Init with a list of rows.
        ====================================================================
        """
        self._data = data
        rows = len(data)
        cols = len(data[0]) if data else 0
        HasRowsCols.__init__(self, rows=rows, cols=cols)

    @property
    def values(self) -> list[list[str]]:
        """
        ====================================================================
         Return the raw row data.
        ====================================================================
        """
        return self._data

    def to_df(self, header: bool = True) -> pd.DataFrame:
        """
        ====================================================================
         Convert to a pandas DataFrame.
         If header=True, the first row is used as column names.
        ====================================================================
        """
        if header and self._data:
            return pd.DataFrame(data=self._data[1:],
                                columns=self._data[0])
        return pd.DataFrame(data=self._data)

    def __getitem__(self, row: int) -> list[str]:
        """
        ====================================================================
         Return a Row by Index (0-based).
        ====================================================================
        """
        return self._data[row]

    def __str__(self, max_rows: int = 10) -> str:
        """
        ====================================================================
         Return a string representation of the Range.
         If more than max_rows, show first and last rows with '...'.
        ====================================================================
        """
        if self.rows <= max_rows:
            return '\n'.join(str(row) for row in self._data)
        half = max_rows // 2
        top = [str(row) for row in self._data[:half]]
        bottom = [str(row) for row in self._data[-half:]]
        return '\n'.join(top + ['...'] + bottom)
