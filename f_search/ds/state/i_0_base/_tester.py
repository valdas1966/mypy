from f_search.ds.state.i_0_base._factory import StateBase


def test_repr() -> None:
    """
    ========================================================================
     Test the __repr__ method.
    ========================================================================
    """
    a = StateBase.Factory.a()
    assert repr(a) == '<StateBase: Key=A>'
