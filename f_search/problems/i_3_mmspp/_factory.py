from f_search.problems.i_3_mmspp.main import ProblemMMSPP, Grid, State


class Factory:
    """
    ============================================================================
     Factory for the ProblemMMSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> ProblemMMSPP:
        """
        ========================================================================
         Return a ProblemMMSPP with a 4x4 GridMap without obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        starts = [State(key=grid[0][0]),
                  State(key=grid[3][0])]
        goals = [State(key=grid[0][3]),
                 State(key=grid[3][3])]
        return ProblemMMSPP(grid=grid, starts=starts, goals=goals)

    @staticmethod
    def with_obstacles() -> ProblemMMSPP:
        """
        ========================================================================
         Return a ProblemMMSPP with a 4x4 GridMap with obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_with_obstacles()
        starts = [State(key=grid[0][0]),
                  State(key=grid[3][0])]
        goals = [State(key=grid[0][3]),
                 State(key=grid[3][3])]
        return ProblemMMSPP(grid=grid, starts=starts, goals=goals)
