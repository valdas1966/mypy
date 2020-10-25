from proj.ai.model.point import Point
from f_utils import u_dict


class LogicPointDistance:

    @staticmethod
    def points_nearest(point_a, points_b):
        """
        ========================================================================
         Description: Return Dict of Points ordered by nearest distance
                        to the Point-A.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point_a : Point
            2. point_b : Set of Points
        ========================================================================
         Return: Dict {Point (Point B) -> int (Manhattan Distance to Point A).
        ========================================================================
        """
        assert type(point_a) == Point, f'type(point_a)={type(point_a)}'
        assert type(points_b) in [tuple, list, set], f'type=(points_b)=' \
                                                     f'{type(points_b)}'
        dict_points = dict()
        for point_b in set(points_b):
            dict_points[point_b] = point_a.distance(point_b)
        return u_dict.sort_by_value(dict_points)
