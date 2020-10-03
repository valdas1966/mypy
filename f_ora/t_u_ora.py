from f_utils import u_tester
from f_ora import u_ora


class Tester_U_Ora:

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_run()
        self.tester_description()
        self.tester_drop()
        self.tester_create_table_as()
        self.tester_add_primary_key()
        self.tester_count()
        self.tester_select()
        self.tester_get_empty_cols()
        u_tester.print_finish(__file__)

    def tester_run(self):
        res_0 = u_ora.run('select * from dual')
        p0 = True if res_0 else False
        res_1 = u_ora.run('xxx')
        p1 = True if not res_1 else False

        u_tester.run([p0, p1])

    def tester_description(self):
        res_0 = u_ora.description('dual')
        p0 = True if res_0 else False
        res_1 = u_ora.description('table_not_exist')
        p1 = True if not res_1 else False

        u_tester.run([p0, p1])

    def tester_drop(self):
        u_ora.create_table_as('temp_u_ora','select * from dual')
        res_drop = u_ora.drop_table('temp_u_ora')
        p0 = True if res_drop else False
        res_drop = u_ora.drop_table('temp_u_ora')
        p1 = True if not res_drop else False
        u_tester.run([p0, p1])

    def tester_create_table_as(self):
        res_0 = u_ora.create_table_as('temp_u_ora',
                                           'select * from dual')
        p0 = True if res_0 else False
        res_1 = u_ora.create_table_as('temp_u_ora','xxx')
        p1 = True if not res_1 else False
        u_tester.run([p0, p1])

    def tester_add_primary_key(self):
        res_0 = u_ora.create_table_as('temp_u_ora','select * from dual','dummy')
        p0 = True if res_0 else False
        u_tester.run([p0])

    def tester_count(self):
        res = u_ora.count('dual')
        p0 = res.val == 1
        u_tester.run([p0])

    def tester_select(self):
        import pandas as pd
        res = u_ora.select('dual')
        df_true = pd.DataFrame.from_dict({'DUMMY': ['X']})
        p0 = res.val.equals(df_true)
        res = u_ora.select('select * from table not exist')
        p1 = True if not res else False
        u_tester.run([p0, p1])

    def tester_get_empty_cols(self):
        tname = 'temp_tester_get_empty_cols'
        query = 'select dummy as col_1, cast(null as int) as col_2 from dual'
        u_ora.create_table_as(tname, query)
        empty_cols_test = u_ora.get_empty_cols(tname)
        empty_cols_true = {'col_2'}
        p0 = empty_cols_test == empty_cols_true
        u_tester.run([p0])


if __name__ == '__main__':
    Tester_U_Ora()
