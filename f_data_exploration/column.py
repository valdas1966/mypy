import pandas as pd
from collections import Counter
from f_utils import u_int
from f_utils import u_float
from f_excel.c_excel import Excel


class Column:

    col_value = 3
    col_count = 4
    col_percent = 5
    row_type = 5
    row_distinct = 6
    row_null = 7
    row_min = 8
    row_max = 9
    row_common = 17

    def __init__(self, df, name):
        """
        ========================================================================
         Description: Constructor. Init Private Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. df : DataFrame
            2. name : str (Column Name)
        ========================================================================
        """
        assert type(df) == pd.DataFrame
        assert type(name) == str
        assert name in df.columns
        self.name = name
        self.values = df[name].tolist()
        self.count_all = len(self.values)
        self.values = [val for val in self.values if not pd.isnull(val)]
        self.count_null = self.count_all - len(self.values)
        self.counter_values = Counter(self.values)
        self.count_distinct = len(self.counter_values)
        self.value_min = (min(self.counter_values)
                          if self.counter_values else None)
        self.value_max = (max(self.counter_values)
                          if self.counter_values else None)
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
        excel.copy_worksheet('Column', self.name)
        excel.ws = excel.wb[self.name]
        self.__to_excel_basic(excel)
        self.__to_excel_common(excel)

    def __to_excel_basic(self, excel):
        """
        ========================================================================
         Description: Fill Excel with Column basic data.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. excel: Excel
        ========================================================================
        """
        assert type(excel) == Excel
        excel.set_value(self.row_type, self.col_count, self.dtype)
        excel.set_value(self.row_distinct, self.col_count, self.count_distinct)
        percent_distinct = round(self.count_distinct / self.count_all, 2)
        excel.set_value(self.row_distinct, self.col_percent, percent_distinct)
        excel.set_value(self.row_null, self.col_count, self.count_null)
        percent_null = round(self.count_null / self.count_all, 2)
        excel.set_value(self.row_null, self.col_percent, percent_null)
        excel.set_value(self.row_min, self.col_count, self.value_min)
        excel.set_value(self.row_max, self.col_count, self.value_max)

    def __to_excel_common(self, excel, n=10):
        assert type(excel) == Excel
        li_common = self.counter_values.most_common(n)
        rows_to_delete = n - len(li_common)
        if rows_to_delete:
            excel.ws.delete_rows(self.row_common, rows_to_delete)
        for i, (value, freq) in enumerate(li_common):
            excel.set_value(self.row_common + i, self.col_value, value)
            excel.set_value(self.row_common + i, self.col_count, freq)
            percent = round(freq / self.count_all, 2)
            excel.set_value(self.row_common + i, self.col_percent, percent)

    def __dtype(self):
        """
        ========================================================================
         Description: Set Column Data-Type.
        ========================================================================
         Return: type
        ========================================================================
        """
        if u_int.are_int(self.values):
            return 'int'
        if u_float.are_float(self.values):
            return 'float'
        return 'str'

