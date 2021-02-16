from f_utils import u_tester
from f_utils import u_float


class TestFloat:

    def __init__(self):
        u_tester.print_start(__file__)
        TestFloat.__tester_are_float()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_are_float():
        values = [0, 1]
        p0 = u_float.are_float(values)
        values = [0, 1, 1.5]
        p1 = u_float.are_float(values)
        values = ['1', '1.5']
        p2 = u_float.are_float(values)
        values = ['1.5', True]
        p3 = u_float.are_float(values)
        values = ['1.5', 'True']
        p4 = not u_float.are_float(values)
        u_tester.run(p0, p1, p2, p3, p4)


if __name__ == '__main__':
    TestFloat()
