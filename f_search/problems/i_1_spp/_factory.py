from f_search.problems.i_1_spp.main import ProblemSPP, Grid, State  


class Factory:
    """
    ============================================================================
     Factory for the ProblemSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> ProblemSPP:
        """
        ========================================================================
         Return a ProblemSPP with a GridMap without obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        start = State(key=grid[0][0])
        goal = State(key=grid[0][3])
        return ProblemSPP(grid=grid, start=start, goal=goal)

    @staticmethod
    def with_obstacles() -> ProblemSPP:
        """
        ========================================================================
         Return a ProblemSPP with a GridMap with obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_with_obstacles()
        start = State(key=grid[0][0])
        goal = State(key=grid[0][3])
        return ProblemSPP(grid=grid, start=start, goal=goal)
    
    @staticmethod
    def for_cached() -> ProblemSPP:
        """
        ========================================================================
         Return a ProblemSPP on a 5x5 grid with a wall at column 3.
         Start=(0,0), Goal=(0,5). Path must detour through row 4.
        ========================================================================
        """
        grid = Grid.Factory.six_with_obstacles()
        start = State(key=grid[0][0])
        goal = State(key=grid[0][5])
        return ProblemSPP(grid=grid, start=start, goal=goal)

    @staticmethod
    def fictive_goal(grid: Grid, start: State) -> ProblemSPP:
        """
        ========================================================================
         Return a fictive goal state.
        ========================================================================
        """
        goal = State.Factory.million()
        return ProblemSPP(grid=grid, start=start, goal=goal)
        