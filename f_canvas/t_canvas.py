from f_utils import u_tester
from c_canvas import Canvas


class TestCanvas:

    def __init__(self):
        u_tester.print_start(__file__)
        TestCanvas.__tester_get_coor()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_get_coor():
        can = Canvas()
        coor_test = can.get_coor((10, 10, 80, 80))
        coor_true = (10, 10, 80, 80)
        p0 = coor_test == coor_true
        can = Canvas((10, 10, 80, 80))
        coor_test = can.get_coor((25, 25, 50, 50))
        coor_true = (30, 30, 40, 40)
        p1 = coor_test == coor_true
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestCanvas()
