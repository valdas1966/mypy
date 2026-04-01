from f_search.algos.i_2_omspp.i_1_incremental.astar import AStarIncremental


def test_astar_incremental():
    """
    ========================================================================
     Test the A* Algorithm for One-to-Many Shortest-Path-Problem.
    ========================================================================
    """
    algo = AStarIncremental.Factory.without_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 6
    assert stats.discovered == 11


def test_heuristic_calcs() -> None:
    """
    ========================================================================
     Test heuristic_calcs counting (frontier updates + discoveries).
    ========================================================================
    """
    algo = AStarIncremental.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.heuristic_calcs == 15
    algo = AStarIncremental.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 8
    assert solution.stats.discovered == 13
    assert solution.stats.heuristic_calcs == 18

def test_for_node_categories() -> None:
    """
    ========================================================================
     Test IncrementalKA* on the node-categories OMSPP problem.
    ========================================================================
    """
    algo = AStarIncremental.Factory.for_node_categories()
    solution = algo.run()
    assert solution


def test_quality_h() -> None:
    """
    ========================================================================
     Test quality_h without obstacles (perfect heuristic).
    ========================================================================
    """
    algo_without = AStarIncremental.Factory.without_obstacles()
    sol_without = algo_without.run()
    assert sol_without.quality_h == 1.0
    algo_with = AStarIncremental.Factory.for_cached()
    sol_with = algo_with.run()
    assert sol_with.quality_h == ((4 / 12) + (5 / 13)) / 2
