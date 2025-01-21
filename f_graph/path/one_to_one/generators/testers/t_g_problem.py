from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne


def test_gen_3x3() -> None:
    """
    ========================================================================
     Test that gen_3x3 creates a 3x3 problem with correct start and goal.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_3x3()
    assert problem.graph._grid.shape() == '(3,3)'
    assert len(problem.graph) == 9
    assert problem.start == problem.graph[0, 0]
    assert problem.goal == problem.graph[2, 2]


def test_gen_4x4() -> None:
    """
    ========================================================================
     Test that gen_4x4 creates a 4x4 problem with correct start and goal.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_4x4()
    assert problem.graph._grid.shape() == '(4,4)'
    assert len(problem.graph) == 14
    assert problem.start == problem.graph[0, 0]
    assert problem.goal == problem.graph[0, 3]
