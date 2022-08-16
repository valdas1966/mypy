from f_utils import u_tester
from f_data_science import u_fs
import pandas as pd


class TestFS:

    def __init__(self):
        u_tester.print_start(__file__)
        TestFS.__tester_drop_correlated_features()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_drop_correlated_features():
        df = pd.DataFrame({'col_1': [1, 2, 3], 'col_2': [4, 6, 9],
                           'col_3': [1, 2, 3], 'col_4': [-1, -2, -3]})
        df_test = u_fs.drop_correlated_features(df)
        df_true = pd.DataFrame({'col_1': [1, 2, 3], 'col_2': [4, 6, 9]})
        p0 = df_test.equals(df_true)
        u_tester.run(p0)


if __name__ == '__main__':
    TestFS()
