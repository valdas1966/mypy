import pandas as pd


class Column:

    def __init__(self, df, name_col):
        assert type(df) == pd.DataFrame
        assert type(name_col) == str
        assert name_col in df.columns

        
