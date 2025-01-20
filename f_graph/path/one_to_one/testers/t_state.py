from f_graph.path.one_to_one.state import State, Node
from f_ds.queues.i_1_priority import QueuePriority
import pytest


@pytest.fixture
def state() -> State:
    """
    ========================================================================
     Create a test State instance with priority queue.
    ========================================================================
    """
    return State(type_queue=QueuePriority)


def test_init(state: State) -> None:
    """
    ========================================================================
     Test State initialization.
    ========================================================================
    """
    assert isinstance(state.generated, QueuePriority)
    assert isinstance(state.explored, set)
    assert state.best is None
