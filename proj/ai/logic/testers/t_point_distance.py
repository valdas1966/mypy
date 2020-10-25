from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.logic.point_distance import LogicPointDistance


class TestLogicPointDistance:

    def __init__(self):
        u_tester.print_start(__file__)
        TestLogicPointDistance.__tester_points_nearest()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_points_nearest():
        point_a = Point(0, 0)
        points_b = {Point(2, 0), Point(0, 1), Point(1, 2)}
        nearest_test = LogicPointDistance.points_nearest(point_a, points_b)
        nearest_true = {Point(0, 1): 1, Point(2, 0): 2, Point(1, 2):3}
        p0 = nearest_test == nearest_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestLogicPointDistance()
