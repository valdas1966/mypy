from f_utils import u_tester
from f_utils import u_int


class TestInt:

    def __init__(self):
        u_tester.print_start(__file__)
        TestInt.__tester_to_percent()
        TestInt.__tester_to_commas()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_to_percent():
        # int example
        count_true = 3
        count_all = 9
        percent_test = u_int.to_percent(count_true, count_all,
                                        to_str=False)
        percent_true = 33
        p0 = percent_test == percent_true
        # float example
        percent_test = u_int.to_percent(count_true, count_all,
                                        precision=2, to_str=False)
        percent_true = 33.33
        p1 = percent_test == percent_true
        # str example
        percent_test = u_int.to_percent(count_true, count_all, to_str=True)
        percent_true = '33%'
        p2 = percent_test == percent_true
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_to_commas():
        n = 1999
        commas_test = u_int.to_commas(n)
        commas_true = '1,999'
        p0 = commas_test == commas_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestInt()
