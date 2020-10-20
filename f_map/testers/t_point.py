from f_utils import u_tester
from f_map.c_point import Point
from f_const.directions import Directions


class TestPoint:

    def __init__(self):
        u_tester.print_start(__file__)
        TestPoint.__tester_eq()
        TestPoint.__tester_direction()
        TestPoint.__tester_ordering()
        # TestPoint.__tester_compass_direction()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_eq():
        p0 = Point(1, 2) == Point(1, 2)
        p1 = Point(1, 2) != Point(3, 4)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_ordering():
        p0 = Point(1, 2) < Point(1, 3)
        p1 = Point(1, 2) < Point(2, 3)
        p2 = Point(1, 2) <= Point(1, 2)
        p3 = Point(1, 2) <= Point(1, 3)
        p4 = Point(1, 2) > Point(0, 0)
        p5 = Point(1, 2) > Point(1, 1)
        p6 = Point(1, 2) >= Point(1, 2)
        p7 = Point(1, 2) >= Point(0, 3)
        u_tester.run(p0, p1, p2, p3, p4, p5, p6, p7)

    @staticmethod
    def __tester_direction():
        point_0 = Point(2, 2)
        point_1 = Point(0, 4)
        point_2 = Point(4, 4)
        point_3 = Point(4, 0)
        point_4 = Point(0, 0)
        direction_test = Point.direction(point_0, point_1)
        p0 = direction_test == 315
        direction_test = Point.direction(point_0, point_2)
        p1 = direction_test == 45
        direction_test = Point.direction(point_0, point_3)
        p2 = direction_test == 135
        direction_test = Point.direction(point_0, point_4)
        p3 = direction_test == 225
        u_tester.run(p0, p1, p2, p3)

    @staticmethod
    def __tester_compass_direction():
        point_0 = Point(2, 2)
        point_1 = Point(0, 4)
        point_2 = Point(4, 4)
        point_3 = Point(4, 0)
        point_4 = Point(0, 0)
        direction_test = Point.compass_direction(point_0, point_1)
        p0 = direction_test == Directions.UP
        direction_test = Point.compass_direction(point_0, point_2)
        p1 = direction_test == Directions.RIGHT
        direction_test = Point.compass_direction(point_0, point_3)
        p2 = direction_test == Directions.DOWN
        direction_test = Point.compass_direction(point_0, point_4)
        p3 = direction_test == Directions.LEFT
        u_tester.run(p0, p1, p2, p3)


if __name__ == '__main__':
    TestPoint()
