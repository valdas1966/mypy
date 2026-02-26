from f_search.ds.data.incremental.main import DataIncremental
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ========================================================================
     Factory for creating DataIncremental test instances.
    ========================================================================
    """

    @staticmethod
    def empty() -> DataIncremental:
        """
        ====================================================================
         Return an empty DataIncremental.
        ====================================================================
        """
        return DataIncremental()

    @staticmethod
    def with_cached() -> DataIncremental:
        """
        ====================================================================
         Return a DataIncremental with cached distances on a 4x4 grid.
         Cached: (0,1)=2, (1,0)=3.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_01 = State(key=grid[0][1])
        s_10 = State(key=grid[1][0])
        dict_cached = {s_01: 2, s_10: 3}
        return DataIncremental(dict_cached=dict_cached)

    @staticmethod
    def with_bounded() -> DataIncremental:
        """
        ====================================================================
         Return a DataIncremental with bounded values on a 4x4 grid.
         Bounded: (1,1)=4, (2,0)=5.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_11 = State(key=grid[1][1])
        s_20 = State(key=grid[2][0])
        dict_bounded = {s_11: 4, s_20: 5}
        return DataIncremental(dict_bounded=dict_bounded)

    @staticmethod
    def with_cached_and_bounded() -> DataIncremental:
        """
        ====================================================================
         Return a DataIncremental with both cached and bounded values.
         Cached: (0,1)=2. Bounded: (1,1)=4.
        ====================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        s_01 = State(key=grid[0][1])
        s_11 = State(key=grid[1][1])
        dict_cached = {s_01: 2}
        dict_bounded = {s_11: 4}
        return DataIncremental(dict_cached=dict_cached,
                               dict_bounded=dict_bounded)
