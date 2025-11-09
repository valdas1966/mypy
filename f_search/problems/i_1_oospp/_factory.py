from f_search.problems.i_1_oospp.main import ProblemOOSPP, Grid, State


class Factory:
    """
    ============================================================================
     Factory for the ProblemOOSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> ProblemOOSPP:
        """
        ========================================================================
         Return a ProblemOOSPP with a GridMap without obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        start = State(key=grid[0][0])
        goal = State(key=grid[0][3])
        return ProblemOOSPP(grid=grid, start=start, goal=goal)

    @staticmethod
    def with_obstacles() -> ProblemOOSPP:
        """
        ========================================================================
         Return a ProblemOOSPP with a GridMap with obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_with_obstacles()
        start = State(key=grid[0][0])
        goal = State(key=grid[0][3])
        return ProblemOOSPP(grid=grid, start=start, goal=goal)
