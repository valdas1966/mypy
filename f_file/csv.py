from __future__ import annotations
import pandas as pd


class CSV:

    def __init__(self, path: str, delimiter: str = ',') -> None:
        """
        ========================================================================
         Initialize the CSV object.
        ========================================================================
        """
        self._path = path
        self._delimiter = delimiter

    @staticmethod
    def from_df(df: pd.DataFrame,
                path: str,
                delimiter: str = ',') -> CSV:
        """
        ========================================================================
         Initialize the CSV object from a pandas DataFrame.
        ========================================================================
        """
        

  