from f_search.problems.i_1_spp import ProblemSPP


def test_reverse() -> None:
    """
    ========================================================================
     Test the reverse() method.
    ========================================================================
    """
    problem = ProblemSPP.Factory.without_obstacles()
    name = 'ProblemSPP-Reversed'
    problem_reversed = problem.reverse(name=name)
    assert problem_reversed.name == name
    assert problem_reversed.start == problem.goal
    assert problem_reversed.goal == problem.start
    assert problem_reversed.grid is problem.grid
