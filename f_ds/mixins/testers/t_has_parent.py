import pytest
from f_ds.mixins.has_parent import HasParent


class Node(HasParent['Node']):
    """Test class implementing HasParent"""
    pass


def test_init() -> None:
    """
    ========================================================================
     Test initialization with and without parent.
    ========================================================================
    """
    # Test init without parent
    node = Node()
    assert node.parent is None

    # Test init with parent
    parent = Node()
    child = Node(parent=parent)
    assert child.parent == parent


def test_parent_property() -> None:
    """
    ========================================================================
     Test parent getter and setter.
    ========================================================================
    """
    node = Node()
    parent = Node()

    # Test setter
    node.parent = parent
    assert node.parent == parent

    # Test setting to None
    node.parent = None
    assert node.parent is None


def test_path_from() -> None:
    """
    ========================================================================
     Test path_from method with various scenarios.
    ========================================================================
    """
    # Create a chain of nodes
    root = Node()
    middle = Node(parent=root)
    leaf = Node(parent=middle)

    # Test path from root
    path = leaf.path_from()
    assert path == [root, middle, leaf]

    # Test path from middle node
    path = leaf.path_from(middle)
    assert path == [middle, leaf]

    # Test path from leaf (self)
    path = leaf.path_from(leaf)
    assert path == [leaf]

    # Test path from unrelated node
    unrelated = Node()
    path = leaf.path_from(unrelated)
    assert path == []

