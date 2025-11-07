from f_graph.nodes.generators.g_1_parent import GenNodeParent


def test_parent_child() -> None:
    """
    ========================================================================
     Test the parent and child old_nodes.
    ========================================================================
    """
    parent, child = GenNodeParent.parent_child()
    assert parent.parent is None
    assert child.parent == parent


def test_path_from_root() -> None:
    """
    ========================================================================
     Test the old_path from root.
    ========================================================================
    """
    parent, child = GenNodeParent.parent_child()
    assert parent.path_from_root() == [parent]
    assert child.path_from_root() == [parent, child]


def test_path_from_node() -> None:
    """
    ========================================================================
     Test the old_path from node.
    ========================================================================
    """
    parent, child = GenNodeParent.parent_child()
    assert parent.path_from_node(parent) == [parent]
    assert parent.path_from_node(child) == []
    assert child.path_from_node(parent) == [parent, child]
    assert child.path_from_node(child) == [child]
