from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.algos.i_2_omspp.i_1_incremental.astar import (
    AStarIncremental)
from f_search.problems.i_2_omspp import ProblemOMSPP


def test_name_algo() -> None:
    """
    ========================================================================
     Test that solution.name_algo matches the Algorithm's Name.
    ========================================================================
    """
    algo = AStarIncrementalBackward.Factory.without_obstacles()
    solution = algo.run()
    assert solution.name_algo == 'AStarIncrementalBackward'


def test_is_valid() -> None:
    """
    ========================================================================
     Test that the backward algorithm finds valid solutions.
    ========================================================================
    """
    algo = AStarIncrementalBackward.Factory.without_obstacles()
    solution = algo.run()
    assert solution


def test_all_goals_solved() -> None:
    """
    ========================================================================
     Test that all goals have sub-solutions.
    ========================================================================
    """
    algo = AStarIncrementalBackward.Factory.without_obstacles()
    solution = algo.run()
    assert len(solution.subs) == len(algo.problem.goals)


def test_with_propagation() -> None:
    """
    ========================================================================
     Test that depth_propagation produces valid results.
    ========================================================================
    """
    algo = (AStarIncrementalBackward
            .Factory.without_obstacles_with_propagation())
    solution = algo.run()
    assert solution


def test_same_path_lengths_as_forward() -> None:
    """
    ========================================================================
     Test that backward finds same number of goals as forward.
    ========================================================================
    """
    algo_fwd = AStarIncremental.Factory.without_obstacles()
    algo_bwd = AStarIncrementalBackward.Factory.without_obstacles()
    solution_fwd = algo_fwd.run()
    solution_bwd = algo_bwd.run()
    assert len(solution_fwd.subs) == len(solution_bwd.subs)


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
        algo_fwd = AStarIncremental(problem=problem)
        algo_bwd = AStarIncrementalBackward(problem=problem)
        sol_fwd = algo_fwd.run()
        sol_bwd = algo_bwd.run()
        # Both should agree on solvability
        assert bool(sol_fwd) == bool(sol_bwd)
        # Compare per-goal optimal path lengths
        if sol_fwd:
            fwd_lengths = algo_fwd.optimal_lengths()
            bwd_lengths = algo_bwd.optimal_lengths()
            for goal in problem.goals:
                assert fwd_lengths[goal] == bwd_lengths[goal]
            n_valid += 1
    # Ensure enough valid instances were tested
    assert n_valid >= 500
