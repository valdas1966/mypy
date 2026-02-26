from f_search.ds.data.incremental import DataIncremental


def test_empty() -> None:
    """
    ========================================================================
     Test that empty DataIncremental has empty dicts.
    ========================================================================
    """
    data = DataIncremental.Factory.empty()
    assert data.dict_cached == {}
    assert data.dict_bounded == {}


def test_with_cached() -> None:
    """
    ========================================================================
     Test that DataIncremental with cached has correct values.
    ========================================================================
    """
    data = DataIncremental.Factory.with_cached()
    assert len(data.dict_cached) == 2
    assert len(data.dict_bounded) == 0


def test_with_bounded() -> None:
    """
    ========================================================================
     Test that DataIncremental with bounded has correct values.
    ========================================================================
    """
    data = DataIncremental.Factory.with_bounded()
    assert len(data.dict_cached) == 0
    assert len(data.dict_bounded) == 2


def test_with_cached_and_bounded() -> None:
    """
    ========================================================================
     Test that DataIncremental with both has correct values.
    ========================================================================
    """
    data = DataIncremental.Factory.with_cached_and_bounded()
    assert len(data.dict_cached) == 1
    assert len(data.dict_bounded) == 1
