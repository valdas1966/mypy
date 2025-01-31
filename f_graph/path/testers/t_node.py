from f_graph.path.node import NodePath as Node


def test_node_init() -> None:
    """
    ============================================================================
     Test that Node initializes with correct attributes.
    ============================================================================
    """
    node = Node[int](uid=1, h=10, name="test")
    assert node.uid == 1
    assert node.h == 10
    assert node.name == "test"
    assert node.parent is None
    assert node.g == 0


def test_node_parent() -> None:
    """
    ============================================================================
     Test parent-child relationship between nodes.
    ============================================================================
    """
    parent = Node(uid=1)
    child = Node(uid=2, parent=parent)
    assert child.parent == parent
    assert child.g == parent.g + 1


def test_node_properties() -> None:
    """
    ============================================================================
     Test node properties return correct values.
    ============================================================================
    """
    node = Node(uid=1, h=5)
    
    # Test g property
    assert isinstance(node.g, int)
    assert node.g == 0
    
    # Test h property
    assert isinstance(node.h, int) 
    assert node.h == 5


def test_node_caching() -> None:
    """
    ============================================================================
     Test node caching functionality.
    ============================================================================
    """
    node = Node(uid=1, is_cached=True)
    assert node.is_cached is True
    
    node = Node(uid=2, is_cached=False)
    assert node.is_cached is False
