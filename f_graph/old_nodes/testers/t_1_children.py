from f_graph.nodes.generators.g_1_children import GenNodeChildren


def test_init() -> None:
    """
    ========================================================================
     Test the initialization of the NodeChildren.
    ========================================================================
    """
    parent, child = GenNodeChildren.parent_child()
    assert parent.children == {child.key: child}
    assert child.children == dict()


def test_remove_child() -> None:
    """
    ========================================================================
     Test the removal of a child.
    ========================================================================
    """ 
    parent, child = GenNodeChildren.parent_child()
    removed = parent.remove_child(child.key)
    assert removed == child
    assert parent.children == dict()
