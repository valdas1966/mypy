from f_graph.old_path.algos.one_to_many.generators.g_problem import GenProblemOneToMany


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


def test_to_singles():
    """
    ========================================================================
     Test the to_singles method.
    ========================================================================
    """
    problem = GenProblemOneToMany.gen_3x3()
    singles = problem.to_singles()
    assert len(singles) == 2
    assert singles[0].graph == problem.graph
    assert singles[0].start == problem.start
    assert singles[0].goal == list(problem.goals)[0]
    assert singles[1].graph == problem.graph
    assert singles[1].start == problem.start
    assert singles[1].goal == list(problem.goals)[1]


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
