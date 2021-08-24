from f_utils import u_tester
from f_math.number import u_integer
from random import randint


class TestInteger:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_div()
        self.__tester_mod()
        self.__tester_digit_at()
        self.__tester_plus()
        self.__tester_minus()
        self.__tester_mult_digit_int()
        self.__tester_mult()
        self.__tester_pow()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_div():
        p0 = True
        for _ in range(1000):
            a = randint(0, 9)
            b = randint(1, 9)
            if u_integer.div(a, b) != a // b:
                p0 = False
                # print(a, b, u_integer.div(a, b))
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_mod():
        p0 = True
        for _ in range(1000):
            a = randint(0, 9)
            b = randint(1, 9)
            if u_integer.mod(a, b) != a % b:
                p0 = False
                # print(a, b, u_integer.mod(a, b))
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_digit_at():
        p0 = True
        for _ in range(1000):
            n = randint(0, 1000000)
            str_n = str(n)[::-1]
            i = randint(0, len(str_n)-1)
            if u_integer.digit_at(n, i) != int(str_n[i]):
                p0 = False
                # print(n, str_n, i, u_integer.digit_at(n, i), str_n[i])
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_plus():
        p0 = True
        for _ in range(1000):
            a = randint(0, 1000)
            b = randint(0, 1000)
            if u_integer.plus(a, b) != (a+b):
                p0 = False
                # print(a, b, u_integer.sum(a, b))
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_minus():
        p0 = True
        for _ in range(1000):
            a = randint(0, 1000)
            b = randint(0, 1000)
            if u_integer.minus(a, b) != (a - b):
                p0 = False
                # print(a, b, u_integer.sum(a, b))
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_mult_digit_int():
        p0 = True
        for _ in range(1000):
            d = randint(0, 9)
            n = randint(0, 999)
            if u_integer.mult_digit_int(d, n) != (d * n):
                p0 = False
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_mult():
        p0 = True
        for _ in range(1000):
            a = randint(0, 1000)
            b = randint(0, 1000)
            if u_integer.mult(a, b) != (a * b):
                p0 = False
                # print(a, b, u_integer.mult(a, b))
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_pow():
        p0 = True
        for _ in range(1000):
            a = randint(0, 10)
            b = randint(0, 3)
            if u_integer.pow(a, b) != a**b:
                p0 = False
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestInteger()
