from f_utils import u_tester
from f_math.number.c_decimal import Decimal


class TestDecimal:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_decimal_point()
        self.__tester_add()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_decimal_point():
        d = Decimal(1)
        p0 = d.decimal_point() == 1
        d = Decimal(1.1)
        p1 = d.decimal_point() == 1
        d = Decimal(1.23)
        p2 = d.decimal_point() == 2
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_add():
        d1, d2 = Decimal(1), Decimal(2)
        p0 = d1 + d2 == 3.0
        d1, d2 = Decimal(1.2), Decimal(3.4)
        p1 = d1 + d2 == 4.6
        d1, d2 = Decimal(1.2), Decimal(3.45)
        p2 = d1 + d2 == 4.65
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestDecimal()
