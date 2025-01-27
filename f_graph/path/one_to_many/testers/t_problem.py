from f_graph.path.one_to_many.generators.g_problem import GenProblemOneToMany


def test_problem_one_to_many():
    """
    ========================================================================
     Test the ProblemOneToMany class.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    graph = problem.graph
    assert problem.start == graph[0, 0]
    assert problem.goals == {graph[0, 2], graph[2, 0]}


def test_clone():
    """
    ========================================================================
     Test the clone method.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    cloned = problem.clone()
    assert cloned == problem
    assert cloned is not problem


def test_key_comparison():
    """
    ========================================================================
     Test the key_comparison method.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    key = problem.key_comparison()
    assert key == (problem.graph, problem.start, problem.goals)
