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


def test_h_start() -> None:
    """
    ========================================================================
     Test the h_start property.
    ========================================================================
    """
    # 4x4 grid, start=(0,0), goal=(0,3) -> Manhattan = 3
    problem = ProblemSPP.Factory.without_obstacles()
    assert problem.h_start == 3


def test_norm_h_start() -> None:
    """
    ========================================================================
     Test the norm_h_start property.
    ========================================================================
    """
    # 4x4 grid, max Manhattan = 4+4-2 = 6, dist=3 -> 3/6*100 = 50.0
    problem = ProblemSPP.Factory.without_obstacles()
    assert problem.norm_h_start == 50.0


def test_to_analytics() -> None:
    """
    ========================================================================
     Test the to_analytics() method.
    ========================================================================
    """
    # 4x4 grid without obstacles, start=(0,0), goal=(0,3)
    problem = ProblemSPP.Factory.with_obstacles()
    d = problem.to_analytics()
    assert d['rows'] == 4
    assert d['cols'] == 4
    assert d['cells'] == 14
    assert d['h_start'] == 3
    assert d['norm_h_start'] == 50.0
    assert 'domain' in d
    assert 'map' in d
