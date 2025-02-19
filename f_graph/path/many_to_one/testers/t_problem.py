from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne


def test_gen_3x3():
    """
    ========================================================================
     Test the generation of a 3x3 Many-to-One problem.
    ========================================================================
    """
    problem = GenProblemManyToOne.gen_3x3()
    graph = problem.graph
    start_1, start_2 = problem._starts
    goal = problem.goal
    problem_1, problem_2 = problem.to_singles()
    assert problem_1.graph == graph
    assert problem_2.graph == graph
    assert problem_1.start == start_1
    assert problem_2.start == start_2
    assert problem_1.goal == goal
    assert problem_2.goal == goal


def test_random() -> None:
    """
    ========================================================================
     Test the generation of a random Many-to-One problem.
    ========================================================================
    """
    problem = GenProblemManyToOne.gen_random(num_rows=4,
                                             pct_invalid=50,
                                             num_starts=2)
    assert len(problem.graph) == 8
    assert len(problem.starts) == 2
    assert len(problem.goal) == 1
