from f_hs.algo.i_1_astar import AStar


def test_graph_abc_path_found() -> None:
    """
    ========================================================================
     Test AStar on A -> B -> C finds the optimal path (cost 2).
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    # Dispatch pin: simple h → stays on simple AStar path.
    assert type(algo) is AStar
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
     Test AStar returns invalid when no path exists.
    ========================================================================
    """
    algo = AStar.Factory.graph_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal() -> None:
    """
    ========================================================================
     Test AStar handles start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = AStar.Factory.graph_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond() -> None:
    """
    ========================================================================
     Test AStar on diamond graph finds optimal path (cost 2).
    ========================================================================
    """
    algo = AStar.Factory.graph_diamond()
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
    algo = AStar.Factory.graph_abc()
    algo.run()
    assert algo.elapsed is not None
    assert algo.elapsed >= 0


def test_search_state() -> None:
    """
    ========================================================================
     The search_state property exposes the dynamic SearchStateSPP.
     After run() it reports the goal_reached and the populated
     g / parent / closed bundle.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    algo.run()
    s = algo.search_state
    assert s.goal_reached is not None
    assert s.goal_reached.key == 'C'
    assert s.g[s.goal_reached] == 2.0
    assert s.parent[s.goal_reached] is not None
    assert s.parent[s.goal_reached].key == 'B'


def test_resume_preserves_state() -> None:
    """
    ========================================================================
     resume() continues the loop without re-initializing —
     closed set after run() is a subset of closed after resume(),
     existing g-values preserved. Verified on graph_diamond,
     where C is pushed-but-not-popped during run() and gets
     popped during resume().
    ========================================================================
    """
    algo = AStar.Factory.graph_diamond()
    algo.run()
    closed_after_run = set(algo.search_state.closed)
    g_after_run = dict(algo.search_state.g)
    assert closed_after_run

    algo.resume()
    closed_after_resume = set(algo.search_state.closed)
    g_after_resume = dict(algo.search_state.g)
    assert closed_after_run.issubset(closed_after_resume)
    assert len(closed_after_resume) > len(closed_after_run)
    for state, g in g_after_run.items():
        assert g_after_resume[state] == g
    assert algo.elapsed is not None
    assert algo.elapsed >= 0


def test_simple_priority_is_3_tuple() -> None:
    """
    ========================================================================
     Simple AStar's priority is a 3-tuple (f, -g, state) — no
     cache_rank. Pins the "fast path" invariant.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    algo.run()
    start = algo.problem.starts[0]
    p = algo._priority(state=start)
    assert len(p) == 3
    assert p[0] == algo.search_state.g[start] + algo._h(start)
