from f_hs.state import StateBase as State


def test_key() -> None:
    """
    ========================================================================
     Test the key property.
    ========================================================================
    """
    state = State[str](key='A')
    assert state.key == 'A'
