from f_search.problems import ProblemOMSPP
from f_search.ds.data.cached.main import DataCached
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ========================================================================
     Factory for creating DataCached test instances.
    ========================================================================
    """

    @staticmethod
    def empty() -> DataCached:
        """
        ====================================================================
         Return an empty DataCached.
        ====================================================================
        """
        return DataCached()

    @staticmethod
    def with_cached() -> DataCached:
        """
        ====================================================================
         Return a DataCached with cached distances on a 4x4 grid.
         Cached: (0,1)=2, (1,0)=3.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_01 = State(key=grid[0][1])
        s_10 = State(key=grid[1][0])
        dict_cached = {s_01: 2, s_10: 3}
        return DataCached(dict_cached=dict_cached)

    @staticmethod
    def with_bounded() -> DataCached:
        """
        ====================================================================
         Return a DataCached with bounded values on a 4x4 grid.
         Bounded: (1,1)=4, (2,0)=5.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_11 = State(key=grid[1][1])
        s_20 = State(key=grid[2][0])
        dict_bounded = {s_11: 4, s_20: 5}
        return DataCached(dict_bounded=dict_bounded)

    @staticmethod
    def with_cached_and_bounded() -> DataCached:
        """
        ====================================================================
         Return a DataCached with both cached and bounded values.
         Cached: (0,1)=2. Bounded: (1,1)=4.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_01 = State(key=grid[0][1])
        s_11 = State(key=grid[1][1])
        dict_cached = {s_01: 2}
        dict_bounded = {s_11: 4}
        return DataCached(dict_cached=dict_cached,
                          dict_bounded=dict_bounded)

    @staticmethod
    def six_cached() -> DataCached:
        """
        =======================================================================
         Return the states on the optimal path as cached with exact dists.
        =======================================================================
        """
        problem = ProblemOMSPP.Factory.for_cached()
        grid = problem.grid
        state_05 = State(grid[0][5])
        state_15 = State(grid[1][5])
        state_25 = State(grid[2][5])
        state_35 = State(grid[3][5])
        state_45 = State(grid[4][5])
        state_44 = State(grid[4][4])
        state_43 = State(grid[4][3])
        state_33 = State(grid[3][3])
        state_23 = State(grid[2][3])
        state_13 = State(grid[1][3])
        state_03 = State(grid[0][3])
        state_02 = State(grid[0][2])
        state_01 = State(grid[0][1])
        dict_cached = {state_05: 0, state_15: 1, state_25: 2, state_35: 3, state_45: 4,
                       state_44: 5, state_43: 6, state_33: 7, state_23: 8, state_13: 9,
                       state_03: 10, state_02: 11, state_01: 12}
        return DataCached(dict_cached=dict_cached)

    @staticmethod
    def six_bounded() -> DataCached:
        """
        =======================================================================
         Return cached states (on optimal path) with a lower bounds (adjacent
          states of the optimal path).
        =======================================================================
        """
        problem = ProblemOMSPP.Factory.for_cached()
        grid = problem.grid
        state_22 = State(grid[2][2])
        state_12 = State(grid[1][2])
        state_11 = State(grid[1][1])
        state_00 = State(grid[0][0])
        dict_bounded = {state_22: 7, state_12: 10, state_11: 11, state_00: 11}
        dict_cached = Factory.six_cached().dict_cached
        return DataCached(dict_cached=dict_cached, dict_bounded=dict_bounded)

    @staticmethod
    def six_bounded_depth_1() -> DataCached:
        """
        =======================================================================
         Return cached states (on optimal path) with a lower bounds (adjacent
          states to optimal path) and adjacent of adjacent.
        =======================================================================
        """
        problem = ProblemOMSPP.Factory.for_cached()
        grid = problem.grid
        state_32 = State(grid[3][2])
        state_21 = State(grid[2][1])
        state_10 = State(grid[1][0])
        state_22 = State(grid[2][2])
        dict_bounded = Factory.six_bounded().dict_bounded
        dict_bounded[state_32] = 8
        dict_bounded[state_21] = 10
        dict_bounded[state_10] = 10
        dict_bounded[state_22] = 9
        dict_cached = Factory.six_cached().dict_cached
        return DataCached(dict_cached=dict_cached, dict_bounded=dict_bounded)

    @staticmethod
    def six_bounded_depth_2() -> DataCached:
        """
        =======================================================================
         Return cached states (on optimal path) with a lower bounds (adjacent
          states to optimal path) and adjacent of adjacent.
        =======================================================================
        """
        problem = ProblemOMSPP.Factory.for_cached()
        grid = problem.grid
        state_20 = State(grid[2][0])
        state_31 = State(grid[3][1])
        dict_bounded = Factory.six_bounded_depth_1().dict_bounded
        dict_bounded[state_20] = 9
        dict_bounded[state_31] = 9
        dict_cached = Factory.six_cached().dict_cached
        return DataCached(dict_cached=dict_cached, dict_bounded=dict_bounded)
