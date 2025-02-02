from f_graph.path.one_to_one.generators.g_state import GenState, QueuePriority


def test_gen_with_priority():
    """
    ============================================================================
     Test State is created with a priority queue.
    ============================================================================
    """
    state = GenState.gen_with_priority()
    assert state.generated == QueuePriority()
    assert state.explored == set()
    assert state.best is None

