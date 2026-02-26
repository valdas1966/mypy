from f_search.algos.i_1_spp.i_3_astar_reusable_flags import (
    AStarReusableFlags)
from f_search.algos.i_1_spp.i_1_astar import AStar
from f_search.problems import ProblemSPP


def test_finds_optimal_path() -> None:
    """
    ========================================================================
     Test that AStarReusableFlags finds a valid solution.
    ========================================================================
    """
    algo = AStarReusableFlags.Factory.without_obstacles()
    solution = algo.run()
    assert solution


def test_same_explored_as_astar() -> None:
    """
    ========================================================================
     Test that AStarReusableFlags explores same count as AStar
      (no incremental data, same behavior).
    ========================================================================
    """
    problem = ProblemSPP.Factory.without_obstacles()
    solution_astar = AStar(problem=problem).run()
    solution_flags = AStarReusableFlags(problem=problem).run()
    assert (solution_flags.stats.explored
            == solution_astar.stats.explored)


def test_with_incremental_data() -> None:
    """
    ========================================================================
     Test that AStarReusableFlags works with pre-filled DataIncremental.
    ========================================================================
    """
    algo = AStarReusableFlags.Factory.without_obstacles_with_data()
    solution = algo.run()
    assert solution


def test_name_algo() -> None:
    """
    ========================================================================
     Test that solution.name_algo matches the Algorithm's Name.
    ========================================================================
    """
    algo = AStarReusableFlags.Factory.without_obstacles()
    solution = algo.run()
    assert solution.name_algo == 'AStarReusableFlags'
