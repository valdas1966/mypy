from f_core.mixins.has.parent import HasParent


def test_parent() -> None:
    """
    ========================================================================
     Test the parent attribute.
    ========================================================================
    """
    a = HasParent.Factory.a()
    b = HasParent.Factory.b()
    assert a.parent is None
    assert b.parent == a


def test_path_from_root() -> None:
    """
    ========================================================================
     Test the path_from_root method.
    ========================================================================
    """
    a = HasParent.Factory.a()
    b = HasParent.Factory.b()
    assert a.path_from_root() == [a]
    assert b.path_from_root() == [a, b]
