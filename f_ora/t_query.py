from f_utils import u_tester
from c_query import Query


class TesterQuery():

    def __init__(self):
        u_tester.print_start(__file__)
        self.tester_select_from()
        self.tester_on()
        self.tester_where()
        self.tester_groupby()
        self.tester_having()
        self.tester_orderby()
        u_tester.print_finish(__file__)

    def tester_select_from(self):
        q_test = Query()
        q_test.Select = 'col_1, col_2'
        q_test.From = 'tname'
        q_true = 'select col_1, col_2 from tname order by 1'
        p0 = str(q_test) == q_true
        u_tester.run([p0])

    def tester_where(self):
        q_test = Query()
        q_test.Select = 'col_1'
        q_test.From = 'tname'
        q_test.Where = 'col_2=col_3'
        q_true = 'select col_1 from tname where col_2=col_3 order by 1'
        p0 = str(q_test) == q_true
        u_tester.run([p0])

    def tester_on(self):
        q_test = Query()
        q_test.Select = 't1.col_1'
        q_test.From = 'tname_1 t1 left join tname_2 t2'
        q_test.On = 't1.col_1=t2.col_1'
        q_test.Where = 't2.col_1 is null'
        q_true = 'select t1.col_1 from tname_1 t1 left join tname_2 t2 on t1.col_1=t2.col_1 where t2.col_1 is null order by 1'
        p0 = str(q_test) == q_true
        u_tester.run([p0])

    def tester_groupby(self):
        # Simple
        q_test = Query()
        q_test.Select = 'col_1, max(col_2), col_3'
        q_test.From = 'tname'
        q_true = 'select col_1, max(col_2), col_3 from tname group by col_1, col_3 order by 1'
        p0 = str(q_test) == q_true
        # With Where and As
        q_test = Query()
        q_test.Select = 'col_1 as c1, count(distinct col_2) as c2'
        q_test.From = 'tname'
        q_test.Where = 'col_1=col_2'
        q_true = 'select col_1 as c1, count(distinct col_2) as c2 from tname where col_1=col_2 group by col_1 order by 1'
        p1 = str(q_test) == q_true
        # Without single columns (only aggregate funcs)
        q_test = Query()
        q_test.Select = 'max(col) as col'
        q_test.From = 'tname'
        q_true = 'select max(col) as col from tname order by 1'
        p2 = str(q_test) == q_true
        u_tester.run([p0, p1, p2])

    def tester_having(self):
        q_test = Query()
        q_test.Select = 'col_1, max(col_2)'
        q_test.From = 'tname'
        q_test.Having = 'max(col_2)>=1'
        q_true = 'select col_1, max(col_2) from tname group by col_1 having max(col_2)>=1 order by 1'
        p0 = str(q_test) == q_true
        u_tester.run([p0])

    def tester_orderby(self):
        q_test = Query()
        q_test.Select = 'col'
        q_test.From = 'tname'
        q_test.Orderby = 'col'
        q_true = 'select col from tname order by col'
        p0 = str(q_test) == q_true
        u_tester.run([p0])


if __name__ == '__main__':
    TesterQuery()
