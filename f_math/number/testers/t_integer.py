from f_utils import u_tester
from f_math.number import u_integer
from random import randint


class TestInteger:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_div()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_div():
        p0 = True
        for _ in range(100):
            a = randint(0, 9)
            b = randint(1, 9)
            if u_integer.div(a, b) != a // b:
                p0 = False
                print(a, b, u_integer.div(a,b))
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestInteger()
