from f_utils import u_tester
from f_math.number import u_digit
from random import randint


class TestDigit:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_sum()
        self.__tester_mult()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_sum():
        p0 = True
        for _ in range(100):
            a = randint(0, 9)
            b = randint(0, 9)
            prev = randint(0, 1)
            sum = a + b + prev
            remainder_true = sum % 10
            whole_true = sum // 10
            remainder_test, whole_test = u_digit.sum(a, b, prev)
            if remainder_test != remainder_true or whole_test != whole_true:
                p0 = False
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_mult():
        p0 = True
        for _ in range(100):
            a = randint(0, 9)
            b = randint(0, 9)
            prev = randint(0, 8)
            mult = a * b + prev
            remainder_true = mult % 10
            whole_true = mult // 10
            remainder_test, whole_test = u_digit.mult(a, b, prev)
            if remainder_test != remainder_true or whole_test != whole_true:
                p0 = False
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestDigit()
