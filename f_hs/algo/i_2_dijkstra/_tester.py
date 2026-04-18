from f_hs.algo.i_2_dijkstra import Dijkstra


def test_graph_abc_path_found() -> None:
    """
    ========================================================================
     Test Dijkstra on A -> B -> C finds the optimal path (cost 2).
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_abc()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = algo.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'C'


def test_no_path() -> None:
    """
    ========================================================================
     Test Dijkstra returns invalid when no path exists.
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal() -> None:
    """
    ========================================================================
     Test Dijkstra handles start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond() -> None:
    """
    ========================================================================
     Test Dijkstra on diamond graph finds optimal path (cost 2).
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_diamond()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = algo.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'D'


def test_elapsed() -> None:
    """
    ========================================================================
     Test elapsed time is set after run.
    ========================================================================
    """
    algo = Dijkstra.Factory.graph_abc()
    algo.run()
    assert algo.elapsed is not None
    assert algo.elapsed >= 0
