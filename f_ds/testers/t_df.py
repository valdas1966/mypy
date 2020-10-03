from f_utils import u_tester
from f_ds import u_df
import pandas as pd


class TestDF:

    def __init__(self):
        u_tester.print_start(__file__)
        TestDF.__tester_remove_duplicated_columns()
        TestDF.__tester_split_to_x_y()
        TestDF.__tester_drop_columns()
        TestDF.__tester_to_dict()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_remove_duplicated_columns():
        # Remove the first redundant column (col_1 in this example).
        col_1 = [1, 2, 3]
        col_2 = [4, 5, 6]
        df = pd.DataFrame({'col_1': col_1, 'col_1': col_2})
        df_test = u_df.remove_duplicated_columns(df)
        df_true = pd.DataFrame({'col_1': col_2})
        p0 = df_test.equals(df_true)
        u_tester.run(p0)

    @staticmethod
    def __tester_split_to_x_y():
        col_1 = [1, 2, 3]
        col_2 = [4, 5, 6]
        label = [1, 0, 1]
        df = pd.DataFrame({'col_1': col_1, 'col_2': col_2, 'label': label})
        x, y = u_df.split_to_x_y(df)
        x_true = pd.DataFrame({'col_1': col_1, 'col_2': col_2})
        y_true = pd.Series(label)
        p0 = x.equals(x_true)
        p1 = y.equals(y_true)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_drop_columns():
        df = pd.DataFrame({'col_1': [1, 2], 'col_2': [3, 4], 'col_3': [5, 6]})
        df = u_df.drop_columns(df, ['col_1', 'col_3'])
        df_true = pd.DataFrame({'col_2': [3, 4]})
        p0 = df.equals(df_true)
        u_tester.run(p0)

    @staticmethod
    def __tester_to_dict():
        df = pd.DataFrame({'col_1': [1, 2, 2], 'col_2': [11, 22, 33]})
        dict_test = u_df.to_dict(df, col_key='col_1', col_val='col_2')
        dict_true = {1: [11], 2: [22, 33]}
        p0 = dict_test == dict_true
        # Default Values
        dict_test = u_df.to_dict(df)
        p1 = dict_test == dict_true
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestDF()

