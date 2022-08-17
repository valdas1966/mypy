import pandas as pd
from f_utils import u_tester
from f_data_processing.model.transpose.base import TransposeBase
from f_data_processing.model.transpose.key_val import TransposeKeyVal


class TestTranspose:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_base()
        self.__tester_key_val()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_base():
        df = pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})
        t = TransposeBase(df=df, col_key='c', col_val='a')
        p0 = list(t._df.columns) == ['c', 'a']
        u_tester.msg('[')
        u_tester.run(p0)

    @staticmethod
    def __tester_key_val():
        df = pd.DataFrame({'key': ['A', 'B', 'B'], 'val': [1, 1, 2]})
        t = TransposeKeyVal(df=df, col_key='key', col_val='val')
        t.run()
        print(t._groups)


if __name__ == '__main__':
    TestTranspose()
