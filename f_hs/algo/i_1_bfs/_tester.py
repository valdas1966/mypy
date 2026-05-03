from f_hs.algo.i_1_bfs import BFS


def test_graph_abc_path_found() -> None:
    """
    ========================================================================
     Test BFS on A -> B -> C finds the optimal path (cost 2).
    ========================================================================
    """
    algo = BFS.Factory.graph_abc()
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
     Test BFS returns invalid when no path exists.
    ========================================================================
    """
    algo = BFS.Factory.graph_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal() -> None:
    """
    ========================================================================
     Test BFS handles start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = BFS.Factory.graph_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond() -> None:
    """
    ========================================================================
     Test BFS on diamond graph finds optimal path (cost 2).
    ========================================================================
    """
    algo = BFS.Factory.graph_diamond()
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
    algo = BFS.Factory.graph_abc()
    algo.run()
    assert algo.elapsed is not None
    assert algo.elapsed >= 0


def test_counters_surface() -> None:
    """
    ========================================================================
     Test BFS exposes the inherited 3-counter surface
     (cnt_push, cnt_pop, cnt_decrease) and that the FIFO
     invariant holds — `decrease` is a no-op so cnt_decrease
     stays at 0 even when `_decrease_g` would be called.
    ========================================================================
    """
    algo = BFS.Factory.graph_abc()
    algo.run()
    c = algo.counters
    assert set(c) == {'cnt_push', 'cnt_pop', 'cnt_decrease'}
    assert c['cnt_pop'] <= c['cnt_push']
    assert c['cnt_pop'] >= 1
    assert c['cnt_decrease'] == 0  # FIFO no-op
    # Same counter survives a re-run on a fresh algo:
    algo2 = BFS.Factory.graph_decrease()
    algo2.run()
    assert algo2.counters['cnt_decrease'] == 0  # FIFO never decreases
