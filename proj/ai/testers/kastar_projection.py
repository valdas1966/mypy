from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.logic.point_distance import LogicPointDistance
from proj.ai.algo.astar import AStar


class KAStarProjection:

    def __init__(self, grid, start, goals):
        """
        ========================================================================
         Description: Constructor - Init the arguments and sort the goals.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
            3. goals : Set of Points
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(start)={type(start)}'
        assert type(goals) in [tuple, list, set], f'type(goals)={type(goals)}'
        self.grid = grid
        self.start = start
        self.goals = LogicPointDistance.points_nearest(start, goals)

    def run(self):
        for goal in self.goals:
            astar = AStar(self.grid, self.start, goal)
            astar.run()