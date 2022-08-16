import pandas as pd


class TransposeKeyVal:

    def __init__(self, df: pd.DataFrame, col_key: str, col_val: str):
        self.df = df
        self.col_key = col_key
        self.col_val = col_val
        self.cols_relevant = self._set_cols_relevant()
        self.df_relevant = self._set_df_relevant()
        self.key = None
        self.val = None


    def run(self):
        for row in self.df_relevant.iterrows():
            index, series = row
            self._set_attrs_from_row(series)

    def _set_cols_relevant(self):
        return [self.col_key, self.col_val]

    def _set_df_relevant(self):
        return self.df[self.cols_relevant]

    def _set_attrs_from_row(self, s: pd.Series):
        self.key = s[self.col_key]
        self.val = s[self.col_val]


df = pd.DataFrame({'a': [1, 2]})
t = TransposeKeyVal(df, 'a', 'b')
t.run()
