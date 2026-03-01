from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.algos.i_2_omspp.i_1_incremental.astar import (
    AStarIncremental)
from f_search.problems.i_2_omspp import ProblemOMSPP


def test_path_start_and_goal() -> None:
    """
    ========================================================================
     Verify that each Path in the Solution starts at the real Start
      and ends at the real Goal.
    ========================================================================
    """
    n_valid = 0
    for _ in range(1000):
        problem = ProblemOMSPP.Factory.custom(rows=10,
                                              pct_obstacles=20,
                                              k=5)
        algo = AStarIncrementalBackward(problem=problem,
                                        need_path=True)
        solution = algo.run()
        if not solution:
            continue
        for goal in problem.goals:
            path = solution.paths[goal]
            assert path.head() == problem.start
            assert path.tail() == goal
        n_valid += 1
    assert n_valid >= 500


def test_random_forward_vs_backward() -> None:
    """
    ========================================================================
     Stress test: 1000 random 10x10 OMSPP problems.
     Verify forward and backward incremental A* produce identical
      optimal path lengths for each goal.
    ========================================================================
    """
    n_valid = 0
    for _ in range(1000):
        problem = ProblemOMSPP.Factory.custom(rows=10,
                                              pct_obstacles=20,
                                              k=5)
        algo_fwd = AStarIncremental(problem=problem, need_path=True)
        algo_bwd = AStarIncrementalBackward(problem=problem,
                                            need_path=True)
        sol_fwd = algo_fwd.run()
        sol_bwd = algo_bwd.run()
        # Both should agree on solvability
        assert bool(sol_fwd) == bool(sol_bwd)
        # Compare per-goal optimal path lengths
        if sol_fwd:
            for goal in problem.goals:
                assert len(sol_fwd.paths[goal]) == \
                       len(sol_bwd.paths[goal])
            n_valid += 1
    # Ensure enough valid instances were tested
    assert n_valid >= 500
