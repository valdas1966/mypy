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
