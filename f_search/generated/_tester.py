from f_search.generated.main import Generated, State


def test_generated() -> None:
    """
    ========================================================================
     Test the Generated class.
    ========================================================================
    """
    generated = Generated.Factory.ab()
    assert generated.pop() == State.Factory.zero()
    assert generated.pop() == State.Factory.one()
