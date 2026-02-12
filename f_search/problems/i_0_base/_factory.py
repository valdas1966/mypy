from f_search.problems.i_0_base.main import ProblemSearch
from f_ds.grids.grid import GridBase as Grid


class Factory:
    """
    ============================================================================
     Factory for the ProblemSearch.
    ============================================================================
    """

    @staticmethod
    def grid_3x3() -> ProblemSearch:
        """
        ========================================================================
         Return a ProblemSearch object with a 3x3 grid.
        ========================================================================
        """
        grid = Grid.Factory.grid_3x3()
        return ProblemSearch(grid=grid, name='3x3')
