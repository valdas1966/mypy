from f_graph.path.one_to_one.generators.g_cache import GenCache, GenProblemOneToOne


def test_gen_3x3():
    """
    ============================================================================
     Test gen_3x3() method.
    ============================================================================
    """
    cache = GenCache.gen_3x3()
    problem = GenProblemOneToOne.gen_3x3()
    goal, pre_goal = problem.goal, problem.pre_goal
    
    # Test goal node
    assert cache[goal].path() == []
    assert cache[goal].distance() == 0
    
    # Test pre-goal node
    assert cache[pre_goal].path() == [goal]
    assert cache[pre_goal].distance() == 1
