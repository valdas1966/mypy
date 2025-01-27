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
    assert problem.pre_goal == problem.graph[1, 2]
