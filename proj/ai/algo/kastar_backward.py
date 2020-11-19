from proj.ai.model.point import Point
from proj.ai.model.grid import Grid
from proj.ai.algo.astar_lookup import AStarLookup
from proj.ai.logic.point_distance import LogicPointDistance as logic


class KAStarBackward:

    def __init__(self, grid, start, goals, next_goal='NEAREST'):
        """
        ========================================================================
         Description: Create KA*-Backward Algorithm (Use Optimal-Path Nodes
                        from previous searches for Lookup).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goals : Tuple | List | Set
            4. next_goal : str (Method to choose the next Goal)
        ========================================================================
        """
        assert issubclass(type(grid), Grid)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        self.closed = set()
        self.grid = grid
        self.start = start
        self.goals = goals
        if next_goal == 'NEAREST':
            self.goals = list(logic.points_nearest(start, goals).keys())

    def run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        lookup = dict()
        self.closed = set()
        for goal in self.goals:
            astar = AStarLookup(self.grid, goal, self.start, lookup)
            astar.run()
            self.closed = self.closed.union(astar.closed)
            lookup.update(astar.lookup_goal())
