from f_core.mixins.has.parent import HasParent


def test_parent_none() -> None:
    """
    ========================================================================
     Test that parent is None when not set.
    ========================================================================
    """
    parent = HasParent.Factory.parent()
    assert parent.parent is None


def test_parent() -> None:
    """
    ========================================================================
     Test that parent is accessible.
    ========================================================================
    """
    child = HasParent.Factory.child()
    assert child.parent is not None


def test_path_from_root_single() -> None:
    """
    ========================================================================
     Test path_from_root for a root object (no parent).
    ========================================================================
    """
    parent = HasParent.Factory.parent()
    path = parent.path_from_root()
    assert path == [parent]


def test_path_from_root_chain() -> None:
    """
    ========================================================================
     Test path_from_root for a child (parent -> child).
    ========================================================================
    """
    child = HasParent.Factory.child()
    path = child.path_from_root()
    assert len(path) == 2
    assert path[0] is child.parent
    assert path[1] is child
