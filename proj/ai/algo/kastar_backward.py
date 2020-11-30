from collections import Counter
from proj.ai.model.point import Point
from proj.ai.model.grid import Grid
from proj.ai.algo.astar_lookup import AStarLookup
from proj.ai.logic.point_distance import LogicPointDistance as logic


class KAStarBackward:

    def __init__(self, grid, start, goals, lookup=dict(),
                 type_next_goal='NEAREST'):
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
            4. lookup : Dict of {Point: int (True-Distance to Start}.
            5. type_next_goal : str (Method to choose the next Goal)
        ========================================================================
        """
        assert issubclass(type(grid), Grid)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        assert type(lookup) == dict
        self.closed = Counter(list())
        self.grid = grid
        self.start = start
        self.goals = goals
        self.lookup = lookup
        if type_next_goal == 'NEAREST':
            self.goals = list(logic.points_nearest(start, goals).keys())
        self.__run()

    def __run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        li_closed = list()
        for goal in self.goals:
            astar = AStarLookup(self.grid, goal, self.start, self.lookup)
            astar.run()
            li_closed = li_closed + list(astar.closed)
            self.lookup.update(astar.lookup_goal())
        self.closed = Counter(li_closed)
