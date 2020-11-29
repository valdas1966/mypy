from proj.ai.model.point import Point
from proj.ai.model.grid import Grid
from proj.ai.algo.astar_lookup import AStarLookup
from proj.ai.algo.kastar_backward import KAStarBackward
from proj.ai.logic.point_distance import LogicPointDistance as logic


class KAStarBi:

    def __init__(self, grid, start, goals,
                 type_forward_goal='NEAREST', type_next_goal='NEAREST'):
        """
        ========================================================================
         Description: Create BiDirectional-KA*.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goals : Tuple | List | Set
            4. type_forward_goal : str (Method to choose the Forward Goal)
            5. type_next_goal : str (Method to choose the Next Goal)
        ========================================================================
        """
        assert issubclass(type(grid), Grid)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        assert type(type_forward_goal) == str
        assert type(type_next_goal) == str
        self.closed = set()
        self.grid = grid
        self.start = start
        self.goals = goals
        self.type_next_goal = type_next_goal
        self.goal_forward = None
        if type_forward_goal == 'NEAREST':
            self.goals = list(logic.points_nearest(start, goals).keys())
            self.goal_forward = self.goals[0]
            self.goals = set(self.goals) - {self.goal_forward}

    def run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        astar = AStarLookup(self.grid, self.start, self.goal_first)
        astar.run()
        lookup = astar.lookup_start()
        kastar = KAStarBackward(self.grid, self.start, self.goals, lookup,
                                self.type_next_goal)
        kastar.run()
        self.closed = astar.closed.union(kastar.closed)
