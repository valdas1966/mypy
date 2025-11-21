from f_search.ds.generated.main import Generated, StateBase


def test_generated() -> None:
    """
    ========================================================================
     Test the Generated class.
    ========================================================================
    """
    generated = Generated.Factory.ab()
    assert generated.pop() == StateBase.Factory.zero()
    assert generated.pop() == StateBase.Factory.one()
