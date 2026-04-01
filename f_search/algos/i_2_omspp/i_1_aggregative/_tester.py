from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative
from f_search.heuristics.phi import UPhi


def test_aggregative() -> None:
    """
    ========================================================================
     Test the A* Aggregative Algorithm.
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 6
    assert stats.discovered == 11
    algo = AStarAggregative.Factory.with_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 8
    assert stats.discovered == 13
    assert stats.heuristic_calcs == 25


def test_for_node_categories() -> None:
    """
    ========================================================================
     Test AggregativeKA* on the node-categories OMSPP problem.
    ========================================================================
    """
    algo = AStarAggregative.Factory.for_node_categories()
    solution = algo.run()
    assert solution


def test_quality_h() -> None:
    """
    ========================================================================
     Test quality_h without obstacles (perfect heuristic).
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    assert solution.quality_h == 1.0


def test_heuristic_calcs() -> None:
    """
    ========================================================================
     Test heuristic_calcs counting (active goals only per discovery).
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    k = len(algo.problem.goals)
    # h_calcs <= discovered * k (equality only if no goals found mid-search)
    assert solution.stats.heuristic_calcs <= solution.stats.discovered * k
    assert solution.stats.heuristic_calcs == 18
    algo = AStarAggregative.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.heuristic_calcs == 25


def test_phi_max() -> None:
    """
    ========================================================================
     Test with max aggregation function.
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles(phi=UPhi.max)
    solution = algo.run()
    assert solution.quality_h == 1.0


def test_phi_mean() -> None:
    """
    ========================================================================
     Test with mean aggregation function.
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles(phi=UPhi.mean)
    solution = algo.run()
    assert solution.quality_h == 1.0
