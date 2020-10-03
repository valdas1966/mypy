from f_grid import u_nodes
from f_astar.c_kastar import KAStar
from f_astar.c_astar_lookup import AStarLookup


class KAStarLookup:
    """
    ============================================================================
     Description: KA* when the path to last Goal is reverse by lookup.
    ============================================================================
    """

    def __init__(self, grid, start, goals):
        """
        ========================================================================
         Description: Constructor - Set the attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : int (Node's Id).
            3. goals : set of int (Set of Nodes' Id).
        ========================================================================
        """
        self.grid = grid
        self.start = start
        # Set the farthest goal to be the goal_backward
        self.goal_backward = u_nodes.get_farthest(grid, start, goals)
        # Set the nearest goals to be the goals_forward
        self.goals_forward = set(goals) - {self.goal_backward}
        self.expanded_nodes = 0
        self.expanded_forward = 0

    def run(self):
        # Forward Run
        kastar = KAStar(self.grid, self.start, self.goals_forward)
        kastar.run()
        self.expanded_forward = len(kastar.closed)
        # Backward Run
        astar = AStarLookup(self.grid, self.goal_backward, self.start,
                            kastar.closed)
        astar.run()
        self.expanded_nodes = len(kastar.closed) + len(astar.closed)

