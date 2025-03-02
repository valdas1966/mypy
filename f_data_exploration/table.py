import pathlib
import pandas as pd
from f_data_exploration.column import Column
from f_excel.old_c_excel import Excel


class Table:

    col_val = 4
    row_name = 3
    row_cols = 4
    row_rows_all = 5
    row_rows_duplicates = 6
    template = str(pathlib.Path().absolute()) + '\\' + 'Table Exploration.xlsx'

    def __init__(self, tname, df):
        """
        ========================================================================
         Description: Constructor. Init Private Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. tname : str
            2. df : DataFrame
        ========================================================================
        """
        assert type(tname) == str
        assert type(df) == pd.DataFrame
        self.tname = tname
        self.df = df
        self.cols_all = 0
        self.rows_all = 0
        self.rows_duplicate = 0
        self.rows_unique = 0
        self.cols = [Column(self.df, col) for col in self.df.columns]
        self.__run()

    def to_excel(self, xlsx):
        """
        ========================================================================
         Description: OutputRequest the Table-Statistics into Excel-File.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. xlsx : str (Path to OutputRequest Excel-File).
        ========================================================================
        """
        excel = Excel(self.template)
        values = [self.tname, self.cols_all, self.rows_all, self.rows_duplicate]
        row_start = self.row_name
        col = self.col_val
        excel.set_values_col(row_start, col, values)
        for col in self.cols:
            col.to_excel(excel)
        excel.save_as(xlsx)
        excel.close()

    def __run(self):
        """
        ========================================================================
         Description: Collect Statistics about the Table.
        ========================================================================
        """
        self.cols_all = len(self.df.columns)
        self.rows_all = len(self.df)
        self.df = self.df.drop_duplicates()
        self.rows_unique = len(self.df)
        self.rows_duplicate = self.rows_all - self.rows_unique
