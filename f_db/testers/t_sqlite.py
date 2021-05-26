import pandas as pd
from f_utils import u_tester
from f_db.c_sqlite import Sqlite


class TestSqlite:

    def __init__(self):
        u_tester.print_start(__file__)
        TestSqlite.__tester_open()
        TestSqlite.__tester_load_and_select()
        TestSqlite.__tester_ctas()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_open():
        sql = Sqlite()
        sql.close()
        p0 = True
        u_tester.run(p0)

    @staticmethod
    def __tester_load_and_select():
        df_true = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        sql = Sqlite()
        sql.load(df=df_true, tname='temp_1')
        df_test = sql.select(query='temp_1')
        sql.close()
        p0 = df_test.equals(df_true)
        u_tester.run(p0)

    @staticmethod
    def __tester_ctas():
        df = pd.DataFrame({'a': [1, 2, 3]})
        sql = Sqlite()
        sql.load(df=df, tname='temp_1')
        sql.ctas(tname='temp_2', query='select sum(a) as a from temp_1')
        df_test = sql.select(query='temp_2')
        df_true = pd.DataFrame({'a': [6]})
        p0 = df_test.equals(df_true)
        u_tester.run(p0)


if __name__ == '__main__':
    TestSqlite()
