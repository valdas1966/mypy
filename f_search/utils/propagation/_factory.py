from f_search.utils.propagation.main import Propagation
from f_search.problems import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ========================================================================
     Factory for creating Propagation test instances.
    ========================================================================
    """

    @staticmethod
    def single_source() -> Propagation:
        """
        ====================================================================
         Single source at (0,0) with value 3, depth 2,
          on a 4x4 grid without obstacles.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        source = State(key=grid[0][0])
        sources = {source: 3}
        excluded = {source}
        return Propagation(sources=sources,
                           excluded=excluded,
                           successors=problem.successors,
                           depth=2)

    @staticmethod
    def multi_source() -> Propagation:
        """
        ====================================================================
         Two sources on opposite corners of a 4x4 grid.
         (0,0) with value 2 and (0,3) with value 4, depth 1.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        s_a = State(key=grid[0][0])
        s_b = State(key=grid[0][3])
        sources = {s_a: 2, s_b: 4}
        excluded = {s_a, s_b}
        return Propagation(sources=sources,
                           excluded=excluded,
                           successors=problem.successors,
                           depth=1)

    @staticmethod
    def single_source_with_prune() -> Propagation:
        """
        ====================================================================
         Single source at (0,0) with value 3, depth 2, prune=1,
          on a 4x4 grid without obstacles.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        source = State(key=grid[0][0])
        sources = {source: 3}
        excluded = {source}
        return Propagation(sources=sources,
                           excluded=excluded,
                           successors=problem.successors,
                           depth=2,
                           prune=lambda state: 1)

    @staticmethod
    def single_source_depth_zero() -> Propagation:
        """
        ====================================================================
         Single source at (0,0) with value 3, depth 0,
          on a 4x4 grid without obstacles.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        problem = ProblemSearch(grid=grid)
        source = State(key=grid[0][0])
        sources = {source: 3}
        excluded = {source}
        return Propagation(sources=sources,
                           excluded=excluded,
                           successors=problem.successors,
                           depth=0)
