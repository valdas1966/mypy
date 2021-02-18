import pandas as pd
from f_utils import u_int
from f_utils import u_float
from f_excel.c_excel import Excel


class Column:

    col_main = 4
    col_sub = 5
    row_type = 3

    def __init__(self, df, name_col):
        """
        ========================================================================
         Description: Constructor. Init Private Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. df : DataFrame
            2. name_col : str
        ========================================================================
        """
        assert type(df) == pd.DataFrame
        assert type(name_col) == str
        assert name_col in df.columns
        self.values = df[name_col].tolist()
        self.values_all = len(self.values)
        self.values = [val for val in self.values if not pd.isnull(val)]
        self.values_null = self.values_all - len(self.values)
        self.dtype = self.__dtype()

    def to_excel(self, excel):
        """
        ========================================================================
         Description: Fill Excel with Column-Statistics.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. excel : Excel
        ========================================================================
        """
        assert type(excel) == Excel
        excel.set_value(self.row_type, self.col_main, self.dtype)

    def __dtype(self):
        """
        ========================================================================
         Description: Set Column Data-Type.
        ========================================================================
         Return: type
        ========================================================================
        """
        if u_int.are_int(self.values):
            return int
        if u_float.are_float(self.values):
            return float
        return str

