from f_search.problems import ProblemOOSPP, Grid, State


class Factory:


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
