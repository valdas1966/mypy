import pytest
from f_ds.mixins.has_children import HasChildren


class Node(HasChildren['Node']):
    """
    ============================================================================
     Node Class.
    ============================================================================
    """
    pass


@pytest.fixture
def parent() -> Node:
    """
    ========================================================================
     Parent Node.
    ========================================================================
    """
    return Node()


@pytest.fixture
def child(parent: Node) -> Node:
    """
    ========================================================================
     Child Node.
    ========================================================================
    """
    node = Node()
    parent.add_child(node)
    return node


def test_children_getter(parent: Node, child: Node) -> None:
    """
    ========================================================================
     Test the children getter.
    ========================================================================
    """
    assert child in parent.children()
    assert len(parent.children()) == 1


def test_add_child(parent: Node) -> None:
    """
    ========================================================================
     Test adding a child.
    ========================================================================
    """
    new_child = Node()
    parent.add_child(new_child)
    assert new_child in parent.children()
    assert len(parent.children()) == 1


def test_remove_child(parent: Node, child: Node) -> None:
    """
    ========================================================================
     Test removing a child.
    ========================================================================
    """
    parent.remove_child(child)
    assert child not in parent.children()
    assert len(parent.children()) == 0
