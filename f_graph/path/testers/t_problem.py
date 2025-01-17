from f_graph.path.one_to_one.generators.gen_problem import GenProblem


def test_copy():
    problem = GenProblem.one_goal_3x3()
    goal = next(iter(problem.goals))
    problem.start.parent = goal
    copied = problem.copy()
    assert problem.start.parent == goal
    assert copied.start.parent is None
