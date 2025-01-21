from f_graph.path.one_to_one.generators.g_state import GenStateOneToOne, GenProblemOneToOne


def test_gen_3x3() -> None:
    """
    ========================================================================
     Test that gen_3x3 creates a state for a 3x3 problem.
    ========================================================================
    """
    state = GenStateOneToOne.gen_3x3()
    assert not state.generated
    assert not state.explored
    problem = GenProblemOneToOne.gen_3x3()
    assert state.best == problem.graph[0, 1]
