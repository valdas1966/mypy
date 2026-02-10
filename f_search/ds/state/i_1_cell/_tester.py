from f_search.ds.state import StateCell as State


def test_str() -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    zero = State.Factory.zero()
    assert str(zero) == '(0,0)'
    zero_other = State.Factory.zero()
    assert zero == zero_other
