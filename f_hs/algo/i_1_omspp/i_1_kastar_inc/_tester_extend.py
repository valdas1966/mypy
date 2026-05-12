import pytest

from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.algo.i_1_omspp.mixins.extendable import (
    ExtendableOMSPP,
    is_extendable,
)
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


# ──────────────────────────────────────────────────
#  Test fixtures (local; mirrors _tester.py style)
# ──────────────────────────────────────────────────


def _line_graph(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C -> D -> E -> F with configurable goal list.
     Used to test multi-goal extend() chains.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': ['D'],
             'D': ['E'], 'E': ['F'], 'F': []},
        start='A',
        goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


_LINE_POS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}


def _grid_4x4_with_goals(keys: list[tuple[int, int]]
                         ) -> ProblemGrid:
    """
    ========================================================================
     4x4 grid (obstacle factory; corners reachable around it)
     with a configurable goal list.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._goals = [p._states[grid[r][c]] for r, c in keys]
    return p


def _manhattan_grid(s, g) -> int:
    return (abs(s.key.row - g.key.row)
            + abs(s.key.col - g.key.col))


# ──────────────────────────────────────────────────
#  1. Capability
# ──────────────────────────────────────────────────


def test_extend_capability_advertised() -> None:
    """
    ========================================================================
     KAStarInc instances satisfy the ExtendableOMSPP protocol.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    assert isinstance(algo, ExtendableOMSPP)
    assert is_extendable(algo)
    assert hasattr(algo, 'extend')
    assert callable(algo.extend)


# ──────────────────────────────────────────────────
#  2. Preconditions
# ──────────────────────────────────────────────────


def test_extend_before_run_raises() -> None:
    """
    ========================================================================
     extend() before run() raises RuntimeError (elapsed is
     still None — algo never executed).
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS))
    with pytest.raises(RuntimeError):
        algo.extend([p._states['D']])


def test_extend_empty_goals_raises() -> None:
    """
    ========================================================================
     extend([]) raises ValueError — empty extension is a
     caller error, not a no-op.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    with pytest.raises(ValueError):
        algo.extend([])


# ──────────────────────────────────────────────────
#  3. Basic extend correctness vs. baseline
# ──────────────────────────────────────────────────


def test_extend_matches_baseline_single_shot() -> None:
    """
    ========================================================================
     run([B, C]) then extend([D, E]) returns the same per-goal
     costs as a single-shot run([B, C, D, E]).
    ========================================================================
    """
    # Single-shot baseline
    p_full = _line_graph(goals=['B', 'C', 'D', 'E'])
    baseline = KAStarInc(problem=p_full, h=_pos_h(_LINE_POS))
    sol_full = baseline.run()
    cost_baseline = {g.key: s.cost for g, s in sol_full.items()}

    # run() + extend()
    p_inc = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p_inc, h=_pos_h(_LINE_POS))
    algo.run()
    sol_extended = algo.extend(
        [p_inc._states['D'], p_inc._states['E']])
    cost_extended = {g.key: s.cost
                     for g, s in sol_extended.items()}

    assert cost_extended == cost_baseline
    assert cost_extended == {'B': 1, 'C': 2, 'D': 3, 'E': 4}


def test_extend_chain_three_calls() -> None:
    """
    ========================================================================
     run([B]) → extend([C]) → extend([D]) → extend([E]).
     Returned Mapping after each call spans ALL goals so far.
    ========================================================================
    """
    p = _line_graph(goals=['B'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS))
    sol1 = algo.run()
    assert {g.key for g in sol1} == {'B'}

    sol2 = algo.extend([p._states['C']])
    assert {g.key for g in sol2} == {'B', 'C'}

    sol3 = algo.extend([p._states['D']])
    assert {g.key for g in sol3} == {'B', 'C', 'D'}

    sol4 = algo.extend([p._states['E']])
    assert {g.key: s.cost for g, s in sol4.items()} == {
        'B': 1, 'C': 2, 'D': 3, 'E': 4,
    }


# ──────────────────────────────────────────────────
#  4. State reuse — counters cumulative AND lower
#     than re-running from scratch
# ──────────────────────────────────────────────────


def test_extend_counters_cumulative() -> None:
    """
    ========================================================================
     Counters after extend() are >= counters after the
     original run() along every axis (extend adds work,
     never subtracts).
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    counters_after_run = dict(algo.counters)

    algo.extend([p._states['D']])
    counters_after_extend = dict(algo.counters)

    for k in ('cnt_h_search', 'cnt_push', 'cnt_pop',
              'cnt_expanded', 'cnt_generated'):
        assert counters_after_extend[k] >= counters_after_run[k]


def test_extend_saves_work_vs_scratch() -> None:
    """
    ========================================================================
     run([B, C, D]) — single-shot — should expand each state
     at most once thanks to the shared SearchStateSPP. The
     run() + extend() path should perform the SAME total
     work (no double-traversal of A, B, C).
    ========================================================================
    """
    p_full = _line_graph(goals=['B', 'C', 'D'])
    single_shot = KAStarInc(problem=p_full,
                            h=_pos_h(_LINE_POS))
    single_shot.run()
    expanded_full = single_shot.counters['cnt_expanded']

    p_inc = _line_graph(goals=['B'])
    algo = KAStarInc(problem=p_inc, h=_pos_h(_LINE_POS))
    algo.run()
    algo.extend([p_inc._states['C'], p_inc._states['D']])

    # Cumulative expansions equal the single-shot total
    # (state reuse worked). A from-scratch re-run on [B,C,D]
    # twice would be ~2× this — the equality proves no
    # repeated expansion.
    assert algo.counters['cnt_expanded'] == expanded_full


# ──────────────────────────────────────────────────
#  5. Lazy re-push at the extend boundary
# ──────────────────────────────────────────────────


def test_extend_repushes_previous_last_goal() -> None:
    """
    ========================================================================
     After run([B, C]), C is the trailing reached goal and
     was NOT lazy-re-pushed (it was "last"). The next
     extend([D]) call must re-push C BEFORE the new goal
     loop starts so the D sub-search can traverse C if
     needed.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS),
                     is_recording=True)
    algo.run()
    # Snapshot push events before extend.
    pushes_before = [e for e in algo.recorder.events
                     if e['type'] == 'push']
    n_pushes_before = len(pushes_before)
    # State C is now on _last_reached_goal.
    assert algo._last_reached_goal is not None
    assert algo._last_reached_goal.key == 'C'

    algo.extend([p._states['D']])

    # Bookkeeping cleared after re-push consumed.
    pushes_after = [e for e in algo.recorder.events
                    if e['type'] == 'push']
    # At least one new push happened — the re-push of C, plus
    # whatever D's sub-search added.
    assert len(pushes_after) > n_pushes_before
    # The first new push event (between run() and extend())
    # is C being re-pushed.
    re_pushed = pushes_after[n_pushes_before]
    assert re_pushed['state'].key == 'C'

    # extend() updated bookkeeping to the new trailing
    # reached goal.
    assert algo._last_reached_goal is not None
    assert algo._last_reached_goal.key == 'D'


def test_extend_after_unreachable_last_no_repush() -> None:
    """
    ========================================================================
     If the prior run's last goal was unreachable,
     _last_reached_goal stays None — there is nothing to
     re-push at the extend() boundary, and
     _repush_last_reached_goal no-ops without error. The
     subsequent sub-search runs normally.
    ========================================================================
    """
    # Line graph but goal X is disconnected.
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': [], 'X': []},
        start='A',
        goal='B',
    )
    p._goals = [p._states['B'], p._states['X']]
    pos = {'A': 0, 'B': 1, 'C': 2, 'X': 99}
    algo = KAStarInc(problem=p, h=_pos_h(pos),
                     is_recording=True)
    sols = algo.run()
    assert sols[p._states['B']].cost == 1
    assert sols[p._states['X']].cost == float('inf')
    # Last goal was unreachable → _last_reached_goal cleared.
    assert algo._last_reached_goal is None
    assert algo._last_algo is None

    # Extend with C — which the X-search expanded as
    # collateral. Hits already_closed fast-path; no error,
    # correct cost. Crucially, no exception from
    # _repush_last_reached_goal even though there's nothing
    # to push.
    sols2 = algo.extend([p._states['C']])
    assert sols2[p._states['C']].cost == 2
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    # B expanded, X unreachable, C already-closed.
    assert [e['reason'] for e in on_goals] == [
        'expanded', 'unreachable', 'already_closed',
    ]


# ──────────────────────────────────────────────────
#  6. Fast-path consistency under extend
# ──────────────────────────────────────────────────


def test_extend_with_already_closed_fast_path() -> None:
    """
    ========================================================================
     run([C]) closes B as collateral. extend([B]) hits the
     already_closed fast-path → reason='already_closed', no
     sub-search resume.
    ========================================================================
    """
    p = _line_graph(goals=['C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS),
                     is_recording=True)
    algo.run()
    sols2 = algo.extend([p._states['B']])
    by_key = {g.key: s for g, s in sols2.items()}
    assert by_key['C'].cost == 2
    assert by_key['B'].cost == 1
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    reasons = [e['reason'] for e in on_goals]
    assert reasons == ['expanded', 'already_closed']


def test_extend_with_already_reached_fast_path() -> None:
    """
    ========================================================================
     run([B, C]) puts B and C in _solutions. extend([B]) —
     re-submitting a known goal — hits the already_reached
     fast-path.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS),
                     is_recording=True)
    algo.run()
    sols2 = algo.extend([p._states['B']])
    # B's cost unchanged.
    by_key = {g.key: s for g, s in sols2.items()}
    assert by_key['B'].cost == 1
    # Last on_goal is the fast-path event for B.
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert on_goals[-1]['reason'] == 'already_reached'
    assert on_goals[-1]['state'].key == 'B'


# ──────────────────────────────────────────────────
#  7. Elapsed accumulation
# ──────────────────────────────────────────────────


def test_extend_accumulates_elapsed() -> None:
    """
    ========================================================================
     algo.elapsed after extend() > algo.elapsed after run().
     Wall-clock accumulates across calls.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    t_after_run = algo.elapsed
    algo.extend([p._states['D']])
    t_after_extend = algo.elapsed
    assert t_after_extend > t_after_run


# ──────────────────────────────────────────────────
#  8. run_nested classmethod convenience
# ──────────────────────────────────────────────────


def test_run_nested_solves_prefix_extending_sequence() -> None:
    """
    ========================================================================
     run_nested([P1, P2, P3]) where each P_i extends the
     previous goal list. Returns an algo whose solutions
     cover all goals in the longest problem.
    ========================================================================
    """
    p1 = _line_graph(goals=['B'])
    p2 = _line_graph(goals=['B', 'C'])
    p3 = _line_graph(goals=['B', 'C', 'D', 'E'])
    algo = KAStarInc.run_nested(
        problems=[p1, p2, p3], h=_pos_h(_LINE_POS))
    by_key = {g.key: s.cost
              for g, s in algo.solutions.items()}
    assert by_key == {'B': 1, 'C': 2, 'D': 3, 'E': 4}


# ──────────────────────────────────────────────────
#  9. Grid-based regression (heavier problem)
# ──────────────────────────────────────────────────


def test_extend_grid_matches_baseline() -> None:
    """
    ========================================================================
     On a 4x4 grid, run + extend yields per-goal costs
     identical to a single-shot run over the full goal
     list. Same h, same problem topology, same costs.
    ========================================================================
    """
    full_keys = [(0, 3), (3, 3), (3, 0)]
    p_full = _grid_4x4_with_goals(full_keys)
    baseline = KAStarInc(problem=p_full, h=_manhattan_grid)
    baseline.run()
    base_costs = {(g.key.row, g.key.col): s.cost
                  for g, s in baseline.solutions.items()}

    p_inc = _grid_4x4_with_goals([(0, 3)])
    algo = KAStarInc(problem=p_inc, h=_manhattan_grid)
    algo.run()
    grid = p_inc.grid
    algo.extend([p_inc._states[grid[3][3]]])
    algo.extend([p_inc._states[grid[3][0]]])
    inc_costs = {(g.key.row, g.key.col): s.cost
                 for g, s in algo.solutions.items()}

    assert inc_costs == base_costs
