from f_search.utils.propagation.main import propagate
from f_search.problems import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ============================================================================
     Factory for creating propagate() test scenarios.
    ============================================================================
    """

    @staticmethod
    def single_source() -> tuple[dict, set, callable, Grid]:
        """
        ========================================================================
         Single source at (0,0) with value 3 on a 4x4 grid.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        source = State(key=grid[0][0])
        sources = {source: 3}
        excluded = {source}
        return sources, excluded, problem.successors, grid

    @staticmethod
    def multi_source() -> tuple[dict, set, callable, Grid]:
        """
        ========================================================================
         Two sources on opposite corners of a 4x4 grid.
         (0,0) with value 2 and (0,3) with value 4.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        s_a = State(key=grid[0][0])
        s_b = State(key=grid[0][3])
        sources = {s_a: 2, s_b: 4}
        excluded = {s_a, s_b}
        return sources, excluded, problem.successors, grid
