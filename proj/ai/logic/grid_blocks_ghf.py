from proj.ai.model.grid import Grid
from proj.ai.model.point import Point


class LogicGridBlocksGHF:

    @staticmethod
    def to_dict_h(grid, goal):
        """
        ========================================================================
         Description: Create Dictionary of Heuristic Values
                        (heuristic distance to the Goal).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. goal : Point
        ========================================================================
         Return: dict {Point -> int} {Point in the Grid -> Heuristic Distance}
        ========================================================================
        """
        assert issubclass(type(grid), Grid), f'type(grid)={type(grid)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        dict_h = dict()
        for point in grid.points():
            dict_h[point] = point.distance(goal)
        return dict_h
