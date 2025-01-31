from f_graph.path.state import State
from f_graph.path.node import NodePath as Node
from f_ds.queues.i_1_priority import QueuePriority as Queue


def test_state_init() -> None:
    """
    ============================================================================
     Test that State initializes with empty collections and None best node.
    ============================================================================
    """
    state = State(Queue)
    assert len(state.generated) == 0
    assert len(state.explored) == 0
    assert state.best is None


def test_state_collections() -> None:
    """
    ============================================================================
     Test that State collections work as expected.
    ============================================================================
    """
    state = State(Queue)
    node = Node(0)
    
    # Test generated queue
    state.generated.push(node)
    assert len(state.generated) == 1
    assert state.generated.pop() == node
    
    # Test explored set
    state.explored.add(node) 
    assert len(state.explored) == 1
    assert node in state.explored


def test_state_best() -> None:
    """
    ============================================================================
     Test setting best node.
    ============================================================================
    """
    state = State(Queue)
    node = Node(0)
    state.best = node
    assert state.best == node
