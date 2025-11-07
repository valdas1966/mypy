from f_graph.old_path.algos.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.old_path.algos.one_to_one.state import QueueFIFO, QueuePriority


def test_priority() -> None:
    """
    ========================================================================
     Test that Priority State initializes correctly.
    ========================================================================
    """
    state = GenStateOneToOne.gen_priority()
    assert isinstance(state.generated, QueuePriority)
    assert len(state.generated) == 1
    assert len(state.explored) == 1
    assert state.best.cell.row == 0
    assert state.best.cell.col == 1


def test_fifo() -> None:
    """
    ========================================================================
     Test that FIFO State initializes correctly.
    ========================================================================
    """
    state = GenStateOneToOne.gen_fifo()
    assert isinstance(state.generated, QueueFIFO)
    assert len(state.explored) == 0
    assert state.best is None
