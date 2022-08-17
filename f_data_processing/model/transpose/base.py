import pandas as pd


class TransposeBase:

    def __init__(self, df: pd.DataFrame, col_key: str, col_val: str):
        self._col_key = col_key
        self._col_val = col_val
        self._df = df[self._cols_relevant]


    @property
    def _cols_relevant(self):
        return [self._col_key, self._col_val]

