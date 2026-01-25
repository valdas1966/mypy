from f_search.ds.state import StateCell


def test_str() -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    zero = StateCell.Factory.zero()
    assert str(zero) == 'Zero(0,0)'
