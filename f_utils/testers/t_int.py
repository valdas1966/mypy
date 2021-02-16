from f_utils import u_tester
from f_utils import u_int


class TestInt:

    def __init__(self):
        u_tester.print_start(__file__)
        TestInt.__tester_to_percent()
        TestInt.__tester_to_commas()
        TestInt.__tester_are_int()
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

    @staticmethod
    def __tester_are_int():
        values = [0, 1]
        p0 = u_int.are_int(values)
        values = [0, 1, 1.5]
        p1 = not u_int.are_int(values)
        values = [0, 1, True]
        p2 = u_int.are_int(values)
        values = [0, 1, 'True']
        p3 = not u_int.are_int(values)
        values = ['0', '1']
        p4 = u_int.are_int(values)
        u_tester.run(p0, p1, p2, p3, p4)


if __name__ == '__main__':
    TestInt()
