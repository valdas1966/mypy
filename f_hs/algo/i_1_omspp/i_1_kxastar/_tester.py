from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.algo.i_1_omspp.i_1_kxastar import KxAStarOMSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


def _graph_abc_multigoal(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C with configurable goal list.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': []},
        start='A',
        goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


_LINE_POS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}


def _manhattan_grid(s, g) -> int:
    return (abs(s.key.row - g.key.row)
            + abs(s.key.col - g.key.col))


# ──────────────────────────────────────────────────
#  1. Lifecycle
# ──────────────────────────────────────────────────


def test_kxastar_single_goal() -> None:
    """
    ========================================================================
     k=1 runs one A* sub-search and returns its solution.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2


def test_kxastar_two_goals_both_expanded() -> None:
    """
    ========================================================================
     goals=[B, C]: two independent sub-searches; both
     reach their respective goal with reason='expanded'.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_recording=True)
    sols = algo.run()
    by_key = {g.key: s for g, s in sols.items()}
    assert by_key['B'].cost == 1
    assert by_key['C'].cost == 2
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert [e['reason'] for e in on_goals] == ['expanded',
                                                'expanded']


def test_kxastar_unreachable_goal() -> None:
    """
    ========================================================================
     Disconnected goal returns cost=inf with reason='unreachable'.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': [], 'X': []},
        start='A',
        goal='B',
    )
    p._goals = [p._states['B'], p._states['X']]
    pos = {'A': 0, 'B': 1, 'X': 99}
    algo = KxAStarOMSPP(problem=p, h=_pos_h(pos), is_recording=True)
    sols = algo.run()
    assert sols[p._states['X']].cost == float('inf')
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert [e['reason'] for e in on_goals] == ['expanded',
                                                'unreachable']


# ──────────────────────────────────────────────────
#  2. Fast-path: already_reached on duplicate
# ──────────────────────────────────────────────────


def test_kxastar_duplicate_goal_fast_path() -> None:
    """
    ========================================================================
     goals=[B, B]: sub-search 1 expands and finalizes B;
     sub-search 2 hits already_reached — NO second A* runs.
     Counters reflect a single A* (cnt_expanded contributed by
     only the first sub-search).
    ========================================================================
    """
    algo = KxAStarOMSPP.Factory.graph_abc_repeated_goal()
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'B': 1}
    # Only one A* ran → only one set of expansions in counters.
    assert algo.counters['cnt_expanded'] == 1


# ──────────────────────────────────────────────────
#  3. NO already_closed fast-path (no shared CLOSED)
# ──────────────────────────────────────────────────


def test_kxastar_no_already_closed_branch() -> None:
    """
    ========================================================================
     k×A* never emits already_closed — no shared CLOSED set.
     goals=[C, B] runs sub-search 1 for C (expanding A, B
     along the way; that state is DISCARDED), then a fresh
     sub-search 2 for B that re-expands A.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_recording=True)
    algo.run()
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    reasons = [e['reason'] for e in on_goals]
    # Both expanded — second sub-search re-expands from start.
    assert reasons == ['expanded', 'expanded']
    # No already_closed in the schema for kxA*.
    assert 'already_closed' not in reasons


# ──────────────────────────────────────────────────
#  4. NO update_frontier emission (no transition)
# ──────────────────────────────────────────────────


def test_kxastar_no_update_frontier_events() -> None:
    """
    ========================================================================
     kxA* has no between-sub-search frontier transition; the
     orchestrator MUST NOT emit update_frontier events.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_recording=True)
    algo.run()
    assert not any(e['type'] == 'update_frontier'
                   for e in algo.recorder.events)


# ──────────────────────────────────────────────────
#  5. Counter scaffold honesty
# ──────────────────────────────────────────────────


def test_kxastar_counter_scaffold() -> None:
    """
    ========================================================================
     KxAStarOMSPP's counter scaffold drops cnt_h_update (no UPDATE
     phase). The counter dict is the honest minimal set.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    keys = set(dict(algo.counters).keys())
    assert 'cnt_h_search' in keys
    assert 'cnt_h_update' not in keys
    assert keys == {
        'cnt_h_search',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
        'mem_open', 'mem_closed', 'mem_total',
    }


def test_kxastar_elapsed_update_is_zero() -> None:
    """
    ========================================================================
     kxA* never enters PHASE_UPDATE — `elapsed_update` stays
     0.0 by construction.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_timing=True)
    algo.run()
    assert algo.elapsed_update == 0.0
    assert algo.elapsed_search > 0.0


# ──────────────────────────────────────────────────
#  6. Per-goal optimality vs. KAStarInc baseline
# ──────────────────────────────────────────────────


def test_kxastar_costs_match_kastarinc() -> None:
    """
    ========================================================================
     Per-goal optimal costs are identical between kxA* and
     kA*_inc (both solve OMSPP optimally; they differ only in
     state-reuse). Cross-check on a non-trivial graph.
    ========================================================================
    """
    p_x = _graph_abc_multigoal(goals=['B', 'C'])
    p_i = _graph_abc_multigoal(goals=['B', 'C'])
    x = KxAStarOMSPP(problem=p_x, h=_pos_h(_LINE_POS))
    i = KAStarInc(problem=p_i, h=_pos_h(_LINE_POS))
    sx = {g.key: s.cost for g, s in x.run().items()}
    si = {g.key: s.cost for g, s in i.run().items()}
    assert sx == si == {'B': 1, 'C': 2}


def test_kxastar_grid_costs_match_kastarinc() -> None:
    """
    ========================================================================
     On a 4x4 obstacle grid, kxA* and kA*_inc agree on every
     per-goal cost. Cumulative `cnt_expanded` for kxA* should
     be >= kA*_inc's (kxA* is the upper-bound baseline).
    ========================================================================
    """
    p_x = ProblemGrid.Factory.grid_4x4_obstacle()
    p_x._goals = [p_x._states[p_x.grid[0][3]],
                  p_x._states[p_x.grid[3][3]]]
    p_i = ProblemGrid.Factory.grid_4x4_obstacle()
    p_i._goals = [p_i._states[p_i.grid[0][3]],
                  p_i._states[p_i.grid[3][3]]]
    x = KxAStarOMSPP(problem=p_x, h=_manhattan_grid)
    i = KAStarInc(problem=p_i, h=_manhattan_grid)
    sx = {(g.key.row, g.key.col): s.cost
          for g, s in x.run().items()}
    si = {(g.key.row, g.key.col): s.cost
          for g, s in i.run().items()}
    assert sx == si
    # kxA* re-expands from scratch — its cumulative
    # cnt_expanded is the upper bound that state-sharing
    # algos beat.
    assert x.counters['cnt_expanded'] >= i.counters[
        'cnt_expanded']


# ──────────────────────────────────────────────────
#  7. Reconstruct path is intentionally empty
# ──────────────────────────────────────────────────


def test_kxastar_reconstruct_path_empty() -> None:
    """
    ========================================================================
     kxA* discards sub-search state; reconstruct_path returns
     [] by design.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    assert algo.reconstruct_path(p._states['B']) == []
    assert algo.reconstruct_path(p._states['C']) == []
