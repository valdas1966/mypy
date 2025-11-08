from f_search.open.main import Open


def test_priority() -> None:
    """
    ========================================================================
     Test the Open.Factory.priority() method.
    ========================================================================
    """
    open = Open.Factory.priority()
    assert open.to_iterable() == ['B', 'A']
