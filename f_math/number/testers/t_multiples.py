from f_utils import u_tester
from f_math.number import u_multiple


class TestMultiple:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_multiples()
        self.__tester_lcm()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_multiples():
        p0 = u_multiple.multiples(2, 3) == {1: 2, 2: 4, 3: 6}
        p1 = u_multiple.multiples(3, 3) == {1: 3, 2: 6, 3: 9}
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_lcm():
        p0 = u_multiple.lcm(2, 3) == 6
        p1 = u_multiple.lcm(2, 4) == 4
        p2 = u_multiple.lcm(2, 2) == 2
        p3 = u_multiple.lcm(4, 6) == 12
        u_tester.run(p0, p1, p2, p3)




if __name__ == '__main__':
    TestMultiple()
