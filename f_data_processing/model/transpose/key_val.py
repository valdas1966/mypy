import pandas as pd
from collections import defaultdict
from f_data_processing.model.transpose.base import TransposeBase


class TransposeKeyVal(TransposeBase):

    def __init__(self, df: pd.DataFrame, col_key: str, col_val: str):
        super().__init__(df=df, col_key=col_key, col_val=col_val)
        self._groups = defaultdict(list)
        self._key = None
        self._val = None

    def run(self):
        for row in self._df.iterrows():
            index, series = row
            self._set_attrs_from_row(series)
            self._add_attrs_to_groups()

    def _set_attrs_from_row(self, s: pd.Series):
        self._key = s[self._col_key]
        self._val = s[self._col_val]

    def _add_attrs_to_groups(self):
        self._groups[self._key].append(self._val)
