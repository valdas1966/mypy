from f_search.algos.i_2_omspp.i_1_repeated.astar_backward import (
    AStarRepeatedBackward)
from f_search.algos.i_2_omspp.i_1_repeated.astar import AStarRepeated
from f_search.problems.i_2_omspp import ProblemOMSPP


def test_name_algo() -> None:
    """
    ========================================================================
     Test that solution.name_algo matches the Algorithm's Name.
    ========================================================================
    """
    algo = AStarRepeatedBackward.Factory.without_obstacles()
    solution = algo.run()
    assert solution.name_algo == 'AStarRepeatedBackward'


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test the backward algorithm without obstacles.
    ========================================================================
    """
    algo = AStarRepeatedBackward.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 3 + 6
    assert solution.stats.discovered == 7 + 11


def test_with_obstacles() -> None:
    """
    ========================================================================
     Test the backward algorithm with obstacles.
    ========================================================================
    """
    algo = AStarRepeatedBackward.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 7 + 8
    assert solution.stats.discovered == 13 + 13


def test_path_length() -> None:
    """
    ========================================================================
     Stress test: verify forward and backward repeated A* produce
      identical optimal path lengths for each goal.
    ========================================================================
    """
    n_valid = 0
    for _ in range(1000):
        problem = ProblemOMSPP.Factory.custom(rows=10,
                                              pct_obstacles=20,
                                              k=5)
        algo_fwd = AStarRepeated(problem=problem,
                                 need_path=True)
        algo_bwd = AStarRepeatedBackward(problem=problem,
                                         need_path=True)
        sol_fwd = algo_fwd.run()
        sol_bwd = algo_bwd.run()
        assert bool(sol_fwd) == bool(sol_bwd)
        if sol_fwd:
            for goal in problem.goals:
                assert len(sol_fwd.paths[goal]) == \
                       len(sol_bwd.paths[goal])
            n_valid += 1
    assert n_valid >= 500
