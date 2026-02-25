from f_search.problems.i_1_spp import ProblemSPP


def test_reverse() -> None:
    """
    ========================================================================
     Test the reverse() method.
    ========================================================================
    """
    problem = ProblemSPP.Factory.without_obstacles()
    reversed_problem = problem.reverse()
    assert reversed_problem.start == problem.goal
    assert reversed_problem.goal == problem.start
    assert reversed_problem.grid is problem.grid


def test_reverse_with_name() -> None:
    """
    ========================================================================
     Test the reverse() method with a custom Name.
    ========================================================================
    """
    problem = ProblemSPP.Factory.without_obstacles()
    reversed_problem = problem.reverse(name='Reversed')
    assert reversed_problem.name == 'Reversed'
    assert reversed_problem.start == problem.goal
    assert reversed_problem.goal == problem.start
