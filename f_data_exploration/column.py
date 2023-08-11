import pandas as pd
from collections import Counter, defaultdict
from f_utils import u_int
from f_utils import u_str
from f_utils import u_float
from f_excel.old_c_excel import Excel


class Column:

    excel = None

    row_first = 5

    row_basic_type = 5
    row_basic_distinct = 6
    row_basic_null = 7
    row_basic_min = 8
    row_basic_max = 9

    col_basic_value = 4
    col_basic_percent = 5

    col_common_value = 11
    col_common_count = 12
    col_common_percent = 13

    col_len_value = 19
    col_len_count = 20
    col_len_percent = 21

    col_regex_value = 27
    col_regex_count = 28
    col_regex_percent = 29

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
        self.count_not_null = len(self.values)
        self.count_null = self.count_all - self.count_not_null
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
        self.excel = excel
        self.excel.copy_worksheet('Column', self.name)
        self.excel.ws = excel.wb[self.name]
        self.__to_excel_basic()
        self.__to_excel_common()
        self.__to_excel_lengths()
        self.__to_excel_regex()

    def __to_excel_basic(self):
        """
        ========================================================================
         Description: Fill Excel with Column basic data.
        ========================================================================
        """
        self.excel.set_value(self.row_basic_type,
                             self.col_basic_value,
                             self.dtype)
        self.excel.set_value(self.row_basic_distinct,
                             self.col_basic_value,
                             self.count_distinct)
        percent_distinct = round(self.count_distinct / self.count_not_null, 2)
        self.excel.set_value(self.row_basic_distinct,
                             self.col_basic_percent,
                             percent_distinct)
        self.excel.set_value(self.row_basic_null,
                             self.col_basic_value,
                             self.count_null)
        percent_null = round(self.count_null / self.count_all, 2)
        self.excel.set_value(self.row_basic_null,
                             self.col_basic_percent,
                             percent_null)
        self.excel.set_value(self.row_basic_min,
                             self.col_basic_value,
                             self.value_min)
        self.excel.set_value(self.row_basic_max,
                             self.col_basic_value,
                             self.value_max)

    def __to_excel_common(self, n=10):
        li_common = self.counter_values.most_common(n)
        """
        rows_to_delete = n - len(li_common)
        if rows_to_delete:
            excel.ws.delete_rows(self.row_common, rows_to_delete)
        """
        for i, (value, freq) in enumerate(li_common):
            self.excel.set_value(self.row_first + i,
                                 self.col_common_value,
                                 value)
            self.excel.set_value(self.row_first + i,
                                 self.col_common_count,
                                 freq)
            percent = round(freq / self.count_not_null, 2)
            self.excel.set_value(self.row_first+i,
                                 self.col_common_percent,
                                 percent)

    def __to_excel_lengths(self, n=10):
        lengths = defaultdict(int)
        for val, freq in self.counter_values.items():
            length = len(str(val))
            lengths[length] += freq
        li_common = Counter(lengths).most_common(n)
        for i, (value, freq) in enumerate(li_common):
            self.excel.set_value(self.row_first + i,
                                 self.col_len_value,
                                 value)
            self.excel.set_value(self.row_first + i,
                                 self.col_len_count,
                                 freq)
            percent = round(freq / self.count_not_null, 2)
            self.excel.set_value(self.row_first+i,
                                 self.col_len_percent,
                                 percent)
            
    def __to_excel_regex(self, n=10):
        d_regex = defaultdict(int)
        for val, freq in self.counter_values.items():
            regex = u_str.to_regex(val)
            d_regex[regex] += freq
        li_common = Counter(d_regex).most_common(n)
        for i, (value, freq) in enumerate(li_common):
            self.excel.set_value(self.row_first + i,
                                 self.col_regex_value,
                                 value)
            self.excel.set_value(self.row_first + i,
                                 self.col_regex_count,
                                 freq)
            percent = round(freq / self.count_not_null, 2)
            self.excel.set_value(self.row_first+i,
                                 self.col_regex_percent,
                                 percent)

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

