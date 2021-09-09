from f_utils import u_tester
from f_math.number.c_fraction import Fraction


class TestFraction:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_init()
        self.__tester_is_proper()
        self.__tester_to_mixed_number()
        self.__tester_simplify()
        self.__tester_reciprocal()
        self.__tester_from_mixed_number()
        self.__tester_normalize()
        self.__tester_str()
        self.__tester_eq()
        self.__tester_plus()
        self.__tester_minus()
        self.__tester_mult()
        self.__tester_truediv()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        f = Fraction(1, 2)
        p0 = f.numerator == 1
        p1 = f.denominator == 2
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_is_proper():
        f0 = Fraction(1, 2)
        p0 = f0.is_proper()
        f1 = Fraction(1, 1)
        p1 = not f1.is_proper()
        f2 = Fraction(2, 1)
        p2 = not f2.is_proper()
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_to_mixed_number():
        f0 = Fraction(1, 2)
        p0 = f0.to_mixed_number() == (0, 1, 2)
        f1 = Fraction(3, 2)
        p1 = f1.to_mixed_number() == (1, 1, 2)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_simplify():
        f0 = Fraction(1, 2)
        p0 = f0.simplify() == Fraction(1, 2)
        f1 = Fraction(2, 6)
        p1 = f1.simplify() == Fraction(1, 3)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_reciprocal():
        p0 = Fraction(1, 2).reciprocal() == Fraction(2, 1)
        u_tester.run(p0)

    @staticmethod
    def __tester_from_mixed_number():
        p0 = Fraction.from_mixed_number(0, 1, 2) == Fraction(1, 2)
        p1 = Fraction.from_mixed_number(1, 1, 2) == Fraction(3, 2)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_normalize():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        f3, f4 = Fraction.normalize(f1, f2)
        p0 = f3 == Fraction(3, 6)
        p1 = f4 == Fraction(2, 6)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_str():
        f = Fraction(1, 2)
        p0 = str(f) == '1/2'
        u_tester.run(p0)

    @staticmethod
    def __tester_eq():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 2)
        f3 = Fraction(1, 3)
        p0 = f1 == f2
        p1 = not f1 == f3
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_plus():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        p0 = (f1 + f2) == Fraction(5, 6)
        u_tester.run(p0)

    @staticmethod
    def __tester_minus():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        p0 = (f1 - f2) == Fraction(1, 6)
        u_tester.run(p0)

    @staticmethod
    def __tester_mult():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        p0 = (f1 * f2) == Fraction(1, 6)
        u_tester.run(p0)

    @staticmethod
    def __tester_truediv():
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        p0 = (f1 / f2) == Fraction(3, 2)
        u_tester.run(p0)


if __name__ == '__main__':
    TestFraction()
