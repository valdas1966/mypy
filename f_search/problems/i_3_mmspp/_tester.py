from f_search.problems.i_3_mmspp import ProblemMMSPP


def test_starts_goals() -> None:
    """
    ========================================================================
     Test starts and goals properties.
    ========================================================================
    """
    problem = ProblemMMSPP.Factory.without_obstacles()
    assert len(problem.starts) == 2
    assert len(problem.goals) == 2
    grid = problem.grid
    assert problem.starts[0].key == grid[0][0]
    assert problem.starts[1].key == grid[3][0]
    assert problem.goals[0].key == grid[0][3]
    assert problem.goals[1].key == grid[3][3]


def test_h_starts() -> None:
    """
    ========================================================================
     Test h_starts property.
    ========================================================================
    """
    # starts=(0,0) and (3,0): Manhattan = 3
    problem = ProblemMMSPP.Factory.without_obstacles()
    assert problem.h_starts == 3.0


def test_h_goals() -> None:
    """
    ========================================================================
     Test h_goals property.
    ========================================================================
    """
    # goals=(0,3) and (3,3): Manhattan = 3
    problem = ProblemMMSPP.Factory.without_obstacles()
    assert problem.h_goals == 3.0


def test_h_cross() -> None:
    """
    ========================================================================
     Test h_cross property.
    ========================================================================
    """
    # (0,0)->(0,3)=3, (0,0)->(3,3)=6, (3,0)->(0,3)=6, (3,0)->(3,3)=3
    # avg = (3+6+6+3)/4 = 4.5
    problem = ProblemMMSPP.Factory.without_obstacles()
    assert problem.h_cross == 4.5


def test_to_omspps() -> None:
    """
    ========================================================================
     Test to_omspps() decomposition.
    ========================================================================
    """
    problem = ProblemMMSPP.Factory.without_obstacles()
    omspps = problem.to_omspps()
    assert len(omspps) == 2
    # First OMSPP: start=(0,0), goals=[(0,3),(3,3)]
    assert omspps[0].start == problem.starts[0]
    assert omspps[0].goals == problem.goals
    # Second OMSPP: start=(3,0), goals=[(0,3),(3,3)]
    assert omspps[1].start == problem.starts[1]
    assert omspps[1].goals == problem.goals
    # All share the same grid
    assert omspps[0].grid is problem.grid
    assert omspps[1].grid is problem.grid


def test_to_mospps() -> None:
    """
    ========================================================================
     Test to_mospps() decomposition (reverse: one per Goal).
    ========================================================================
    """
    problem = ProblemMMSPP.Factory.without_obstacles()
    mospps = problem.to_mospps()
    assert len(mospps) == 2
    # First MOSPP: start=goal(0,3), goals=[start(0,0), start(3,0)]
    assert mospps[0].start == problem.goals[0]
    assert mospps[0].goals == problem.starts
    # Second MOSPP: start=goal(3,3), goals=[start(0,0), start(3,0)]
    assert mospps[1].start == problem.goals[1]
    assert mospps[1].goals == problem.starts
    # All share the same grid
    assert mospps[0].grid is problem.grid
    assert mospps[1].grid is problem.grid


def test_to_spps() -> None:
    """
    ========================================================================
     Test to_spps() decomposition.
    ========================================================================
    """
    problem = ProblemMMSPP.Factory.without_obstacles()
    spps = problem.to_spps()
    # 2 starts x 2 goals = 4 SPPs
    assert len(spps) == 4
    assert spps[0].start == problem.starts[0]
    assert spps[0].goal == problem.goals[0]
    assert spps[1].start == problem.starts[0]
    assert spps[1].goal == problem.goals[1]
    assert spps[2].start == problem.starts[1]
    assert spps[2].goal == problem.goals[0]
    assert spps[3].start == problem.starts[1]
    assert spps[3].goal == problem.goals[1]


def test_to_analytics() -> None:
    """
    ========================================================================
     Test to_analytics() method.
    ========================================================================
    """
    problem = ProblemMMSPP.Factory.without_obstacles()
    d = problem.to_analytics()
    assert d['rows'] == 4
    assert d['cols'] == 4
    assert d['h_starts'] == 3.0
    assert d['h_goals'] == 3.0
    assert d['h_cross'] == 4.5
    assert 'norm_h_starts' in d
    assert 'norm_h_goals' in d
    assert 'norm_h_cross' in d
