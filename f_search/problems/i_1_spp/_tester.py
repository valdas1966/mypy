from f_search.problems.i_1_spp.main import ProblemSPP


def test_str() -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    problem = ProblemSPP.Factory.without_obstacles()
    assert str(problem) == 'ProblemSPP(Grid4x4(4x4, 16), Start(0,0), Goal(0,3))'
