from f_search.problems.i_1_neighborhood.main import ProblemNeighborhood
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ============================================================================
     Factory for the ProblemNeighborhood.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> ProblemNeighborhood:
        """
        ========================================================================
         Return a ProblemNeighborhood without obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        start = State(key=grid[0][0])
        max_step = 1
        return ProblemNeighborhood(grid=grid, start=start, steps_max=max_step)
