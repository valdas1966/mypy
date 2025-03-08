from f_ds.nodes.generators.g_2_hierarchy import GenNodeHierarchy


def test_parent_child() -> None:
    """
    ========================================================================
     Test the parent and child nodes.
    ========================================================================
    """
    parent, child = GenNodeHierarchy.parent_child()
    assert parent.parent is None
    assert parent.children == {child.key: child}
    assert child.parent == parent
    assert child.children == dict()


def test_remove_child() -> None:
    """
    ========================================================================
     Test the removal of a child.
    ========================================================================
    """ 
    parent, child = GenNodeHierarchy.parent_child()
    removed = parent.remove_child(key=child.key)
    assert removed == child
    assert parent.children == dict()
    assert child.parent is None


def test_add_child() -> None:
    """
    ========================================================================
     Test the addition of a child.
    ========================================================================
    """ 
    parent, child = GenNodeHierarchy.parent_child()
    parent.remove_child(child=child)
    parent.add_child(child=child)
    assert parent.children == {child.key: child}
    assert child.parent == parent
