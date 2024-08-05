import pandas as pd
from f_utils import u_tester
from s_ora.c_ora import Ora


class TestCOra:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_open()
        self.tester_run()
        self.tester_description()
        self.tester_count()
        self.tester_close()
        self.tester_select()
        self.tester_df_to_signature_cols()
        u_tester.print_finish(__file__)

    def tester_open(self):
        ora = Ora()
        res = ora.open()
        ora.close()
        p0 = True if res else False

        ora = Ora('xxx')
        res = ora.open()
        ora.close()
        p1 = True if not res else False

        u_tester.run([p0, p1])

    def tester_run(self):
        ora = Ora()
        ora.open()
        res = ora.run('select * from dual')
        p0 = True if res else False
        res = ora.run('xxx')
        p1 = True if not res else False
        ora.close()

        u_tester.run([p0, p1])

    def tester_description(self):
        ora = Ora()
        ora.open()
        res = ora.description('dual')
        p0 = True if res else False
        res = ora.description('table not exist')
        p1 = True if not res else False
        ora.close()

        u_tester.run([p0, p1])

    def tester_count(self):
        ora = Ora()
        ora.open()
        res_1 = ora.count('dual')
        res_2 = ora.count('table not exist')
        ora.close()
        p0 = res_1.val == 1
        p1 = True if not res_2 else False
        u_tester.run([p0, p1])

    def tester_select(self):
        import pandas as pd
        ora = Ora()
        ora.open()
        res_1 = ora.select('dual')
        res_2 = ora.select('table not exists')
        ora.close()
        p0 = res_1.val.equals(pd.DataFrame.from_dict({'DUMMY': ['X']}))
        p1 = True if not res_2 else False
        u_tester.run([p0, p1])

    def tester_close(self):
        ora = Ora()
        ora.open()
        res = ora.close()
        p0 = True if res else False

        u_tester.run(p0)

    def tester_df_to_signature_cols(self):
        dict_data = {'col_1': [1, 2], 'col_2': [1, 'list'], 'col_3': [1, 1.2]}
        df = pd.DataFrame(dict_data)
        signature_cols = Ora.df_to_signature_cols(df)
        signature_cols_true = 'col_1 int, col_2 varchar2(100), col_3 float'
        p0 = signature_cols == signature_cols_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestCOra()
