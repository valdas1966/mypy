from f_astar.c_astar_lookup import AStarLookup


class AStarBi:
    """
    ============================================================================
     Description: Bi-Directional A* (one turn each direction).
    ============================================================================
    """

    def __init__(self, grid, start, goal):
        """
        ========================================================================
         Description: Constructor (inits the attributes).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start Id).
            3. goal : int (Goal Id).
        ========================================================================
        """
        self.astar_fore = AStarLookup(grid, start, goal)
        self.astar_back = AStarLookup(grid, goal, start)
        self.expanded_nodes = 0
        self.len_optimal = 0

    def run(self):
        """
        ========================================================================
         Description: Run the algorithm (one turn on each direction).
        ========================================================================
        """
        while not self.astar_fore.is_found and not self.astar_back.is_found:
            self.astar_fore.next_move(self.astar_back.best)
            if self.astar_fore.is_found:
                break
            self.astar_back.next_move(self.astar_fore.best)
        closed_union = self.astar_fore.closed.union(self.astar_back.closed)
        self.expanded_nodes = len(closed_union)
        self.len_optimal = self.astar_fore.len_optimal + \
                           self.astar_back.len_optimal

    def idds_closed(self):
        """
        ========================================================================
         Description: Return Set of Idds in Closed sets of Forward and Backward.
        ========================================================================
         Return: set of int.
        ========================================================================
        """
        closed_fore = {node.idd for node in self.astar_fore.closed}
        closed_back = {node.idd for node in self.astar_back.closed}
        return closed_fore.union(closed_back)
