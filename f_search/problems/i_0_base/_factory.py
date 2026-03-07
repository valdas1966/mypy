from f_search.problems.i_0_base.main import ProblemSearch
from f_ds.grids.grid import GridMap as Grid


class Factory:
    """
    ============================================================================
     Factory for the ProblemSearch.
    ============================================================================
    """

    @staticmethod
    def four_with_obstacles() -> ProblemSearch:
        grid = Grid.Factory.four_with_obstacles()
        return ProblemSearch(grid=grid, name='Problem with Obstacles')
