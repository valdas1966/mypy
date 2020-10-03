from f_utils import u_tester
from f_ds import u_fe
import pandas as pd


class TestFE:

    def __init__(self):
        u_tester.print_start(__file__)
        TestFE.__tester_synthetic()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_synthetic():
        df = pd.DataFrame({'col_1': [1, 3], 'col_2': [2, 4]})
        df_test = u_fe.synthetic(df)
        df_true = pd.DataFrame({'col_1_plus_col_2': [3, 7],
                                'col_1_minus_col_2': [-1, -1],
                                'col_1_mult_col_2': [2, 12],
                                'col_1_divide_col_2': [0.5, 0.75],
                                'col_2_minus_col_1': [1, 1],
                                'col_2_divide_col_1': [2, 4/3]})
        p0 = df_test.equals(df_true)
        u_tester.run(p0)


if __name__ == '__main__':
    TestFE()