from f_utils import u_tester
from f_math import u_numbers


class TestNumbers:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_factors()
        self.__tester_common_factors()
        self.__tester_gcf()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_factors():
        p0 = u_numbers.factors(1) == [1]
        p1 = u_numbers.factors(2) == [1, 2]
        p2 = u_numbers.factors(3) == [1, 3]
        p3 = u_numbers.factors(4) == [1, 2, 4]
        p4 = u_numbers.factors(6) == [1, 2, 3, 6]
        u_tester.run(p0, p1, p2, p3, p4)

    @staticmethod
    def __tester_common_factors():
        p0 = u_numbers.common_factors(1, 2) == [1]
        p1 = u_numbers.common_factors(2, 4) == [1, 2]
        p2 = u_numbers.common_factors(4, 4) == [1, 2, 4]
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_gcf():
        p0 = u_numbers.gcf(1, 2) == 1
        p1 = u_numbers.gcf(2, 2) == 2
        p2 = u_numbers.gcf(4, 6) == 2
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestNumbers()
