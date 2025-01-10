import pytest
from f_ds.nodes.mixins.has_parent import HasParent


class Node(HasParent['Node']):
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


def test_parent_getter(root: Node, middle: Node, leaf: Node) -> None:
    """
    ========================================================================
     Test the parent getter.
    ========================================================================
    """
    assert root.parent is None
    assert middle.parent == root
    assert leaf.parent == middle


def test_parent_setter(root: Node, middle: Node) -> None:
    """
    ========================================================================
     Test the parent setter.
    ========================================================================
    """
    middle.parent = None
    assert middle.parent is None
    middle.parent = root
    assert middle.parent == root


def test_path_from_root(root: Node, middle: Node, leaf: Node) -> None:
    """
    ========================================================================
     Test the path from root.
    ========================================================================
    """
    path = leaf.path_from_root()
    assert path == [root, middle, leaf]
    
    path = middle.path_from_root() 
    assert path == [root, middle]
    
    path = root.path_from_root()
    assert path == [root]


def test_path_from_node(root: Node, middle: Node, leaf: Node) -> None:
    """
    ========================================================================
     Test the path from node.
    ========================================================================
    """
    path = leaf.path_from_node(node=middle)
    assert path == [middle, leaf]
    
    path = leaf.path_from_node(node=root)
    assert path == [root, middle, leaf]
    
    path = middle.path_from_node(node=root)
    assert path == [root, middle]

    path = root.path_from_node(node=root)
    assert path == [root]

    path = root.path_from_node(node=leaf)
    assert path == []
