from f_search.ds.data.cached import DataCached
from f_search.ds.state.i_1_cell.main import StateCell as State
from f_ds.grids import GridMap as Grid


def test_empty() -> None:
    """
    ========================================================================
     Test that empty DataCached has empty dicts.
    ========================================================================
    """
    data = DataCached.Factory.empty()
    assert data.dict_cached == {}
    assert data.dict_bounded == {}


def test_with_cached() -> None:
    """
    ========================================================================
     Test that DataCached with cached has correct values.
    ========================================================================
    """
    data = DataCached.Factory.with_cached()
    assert len(data.dict_cached) == 2
    assert len(data.dict_bounded) == 0


def test_with_bounded() -> None:
    """
    ========================================================================
     Test that DataCached with bounded has correct values.
    ========================================================================
    """
    data = DataCached.Factory.with_bounded()
    assert len(data.dict_cached) == 0
    assert len(data.dict_bounded) == 2


def test_with_cached_and_bounded() -> None:
    """
    ========================================================================
     Test that DataCached with both has correct values.
    ========================================================================
    """
    data = DataCached.Factory.with_cached_and_bounded()
    assert len(data.dict_cached) == 1
    assert len(data.dict_bounded) == 1


def test_data_state() -> None:
    """
    ========================================================================
     Test the data_state() method.
    ========================================================================
    """
    grid = Grid.Factory.four_without_obstacles()
    s_01 = State(key=grid[0][1])
    s_11 = State(key=grid[1][1])
    data = DataCached.Factory.with_cached_and_bounded()
    assert data.data_state(s_01) == {'key': s_01.key,
                                     'is_cached': True,
                                     'is_bounded': False}
    assert data.data_state(s_11) == {'key': s_11.key,
                                     'is_cached': False,
                                     'is_bounded': True}
