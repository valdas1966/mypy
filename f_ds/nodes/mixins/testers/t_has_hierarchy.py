import pytest
from f_ds.nodes.mixins.has_hierarchy import HasHierarchy


class Node(HasHierarchy['Node']):
    """
    ============================================================================
     Node Class.
    ============================================================================
    """
    pass


@pytest.fixture
def root() -> Node:
    """
    ========================================================================
     Root Node.
    ========================================================================
    """
    return Node()


@pytest.fixture
def middle(root: Node) -> Node:
    """
    ========================================================================
     Middle Node.
    ========================================================================
    """
    node = Node(parent=root)
    return node


@pytest.fixture
def leaf(middle: Node) -> Node:
    """
    ========================================================================
     Leaf Node.
    ========================================================================
    """
    node = Node(parent=middle)
    return node


def test_add_child_updates_parent(root: Node) -> None:
    """
    ========================================================================
     Test that adding a child updates its parent.
    ========================================================================
    """
    child = Node()
    root.add_child(child)
    assert child.parent == root


def test_remove_child_updates_parent(root: Node, middle: Node) -> None:
    """
    ========================================================================
     Test that removing a child updates its parent.
    ========================================================================
    """
    root.remove_child(middle)
    assert middle.parent is None


def test_set_parent_updates_children(root: Node) -> None:
    """
    ========================================================================
     Test that setting a parent updates children list.
    ========================================================================
    """
    child = Node()
    child.parent = root
    assert child in root.children()


def test_prevent_duplicate_child(root: Node, middle: Node) -> None:
    """
    ========================================================================
     Test that a child cannot be added twice.
    ========================================================================
    """
    root.add_child(middle)  # middle is already a child from fixture
    assert len(root.children()) == 1
    assert middle in root.children()
