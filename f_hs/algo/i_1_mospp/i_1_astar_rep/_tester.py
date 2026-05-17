from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


def _line_problem(start_keys: list[str], goal_key: str
                  ) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C -> D -> E -> F line graph with configurable
     start list and a single goal.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': ['D'],
             'D': ['E'], 'E': ['F'], 'F': []},
        start=start_keys[0],
        goal=goal_key,
    )
    p._starts = [p._states[k] for k in start_keys]
    p._goals = [p._states[goal_key]]
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


def test_kxastar_mospp_single_start() -> None:
    """
    ========================================================================
     k=1 runs one A* sub-search and returns its solution.
    ========================================================================
    """
    p = _line_problem(start_keys=['A'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS))
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2


def test_kxastar_mospp_two_starts_both_expanded() -> None:
    """
    ========================================================================
     starts=[A, B], goal=C: two independent sub-searches.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_recording=True)
    sols = algo.run()
    by_key = {s.key: v for s, v in sols.items()}
    assert by_key['A'].cost == 2
    assert by_key['B'].cost == 1
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    assert [e['reason'] for e in on_starts] == ['expanded',
                                                 'expanded']
    assert [e['start_index'] for e in on_starts] == [0, 1]
    assert [e['state'].key for e in on_starts] == ['A', 'B']


def test_kxastar_mospp_unreachable_start() -> None:
    """
    ========================================================================
     A start with no path to the goal returns cost=inf with
     reason='unreachable'.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': [], 'X': []},
        start='A', goal='B',
    )
    p._starts = [p._states['A'], p._states['X']]
    p._goals = [p._states['B']]
    pos = {'A': 0, 'B': 1, 'X': 99}
    algo = AStarRepMOSPP(problem=p, h=_pos_h(pos),
                        is_recording=True)
    sols = algo.run()
    assert sols[p._states['X']].cost == float('inf')
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    assert [e['reason'] for e in on_starts] == ['expanded',
                                                 'unreachable']


# ──────────────────────────────────────────────────
#  2. Fast-path: already_reached on duplicate start
# ──────────────────────────────────────────────────


def test_kxastar_mospp_duplicate_start_fast_path() -> None:
    """
    ========================================================================
     starts=[A, A]: sub-search 1 finalizes A; sub-search 2
     hits already_reached. Counters reflect a single A*.
    ========================================================================
    """
    algo = AStarRepMOSPP.Factory.graph_abc_repeated_start()
    sols = algo.run()
    by_key = {s.key: v.cost for s, v in sols.items()}
    assert by_key == {'A': 1}
    assert algo.counters['cnt_expanded'] == 1


# ──────────────────────────────────────────────────
#  3. NO already_closed branch (no shared CLOSED)
# ──────────────────────────────────────────────────


def test_kxastar_mospp_no_already_closed_branch() -> None:
    """
    ========================================================================
     kxA*-MOSPP never emits already_closed — no shared CLOSED
     set across sub-searches.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_recording=True)
    algo.run()
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    reasons = [e['reason'] for e in on_starts]
    assert 'already_closed' not in reasons
    assert reasons == ['expanded', 'expanded']


# ──────────────────────────────────────────────────
#  4. NO update_frontier emission
# ──────────────────────────────────────────────────


def test_kxastar_mospp_no_update_frontier_events() -> None:
    """
    ========================================================================
     kxA*-MOSPP has no between-sub-search transition; MUST
     NOT emit update_frontier events.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_recording=True)
    algo.run()
    assert not any(e['type'] == 'update_frontier'
                   for e in algo.recorder.events)


# ──────────────────────────────────────────────────
#  5. Counter scaffold honesty
# ──────────────────────────────────────────────────


def test_kxastar_mospp_counter_scaffold() -> None:
    """
    ========================================================================
     AStarRepMOSPP's scaffold drops cnt_h_update (no UPDATE
     phase). Honest minimal set.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    keys = set(dict(algo.counters).keys())
    assert 'cnt_h_search' in keys
    assert 'cnt_h_update' not in keys
    assert keys == {
        'cnt_h_search',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
        'mem_open', 'mem_closed',
    }


def test_kxastar_mospp_elapsed_update_is_zero() -> None:
    """
    ========================================================================
     kxA*-MOSPP never enters PHASE_UPDATE — elapsed_update
     stays 0.0 by construction.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_timing=True)
    algo.run()
    assert algo.elapsed_update == 0.0
    assert algo.elapsed_search > 0.0


# ──────────────────────────────────────────────────
#  6. Multi-goal problem rejected (MOSPP needs k=1 goal)
# ──────────────────────────────────────────────────


def test_kxastar_mospp_rejects_multi_goal_problem() -> None:
    """
    ========================================================================
     AStarRepMOSPP requires exactly one goal. A multi-goal
     problem raises ValueError at construction.
    ========================================================================
    """
    import pytest
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': []},
        start='A', goal='C',
    )
    p._starts = [p._states['A']]
    p._goals = [p._states['B'], p._states['C']]   # 2 goals
    with pytest.raises(ValueError):
        AStarRepMOSPP(problem=p,
                     h=lambda s, g: 0)


# ──────────────────────────────────────────────────
#  7. Path reconstruction unsupported by design
# ──────────────────────────────────────────────────


def test_kxastar_mospp_reconstruct_path_empty() -> None:
    """
    ========================================================================
     reconstruct_path returns [] — sub-search bundles
     discarded.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    assert algo.reconstruct_path(p._states['A']) == []
    assert algo.reconstruct_path(p._states['B']) == []


# ──────────────────────────────────────────────────
#  8. h-function fixed-goal property
# ──────────────────────────────────────────────────


def test_kxastar_mospp_h_is_fixed_across_subsearches() -> None:
    """
    ========================================================================
     Unlike OMSPP (h varies per sub-search), MOSPP h is closed
     once over the shared goal. The wrapped h callable is the
     SAME object across sub-searches.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='C')
    algo = AStarRepMOSPP(problem=p, h=_pos_h(_LINE_POS))
    h_before = algo._h_wrapped
    algo.run()
    h_after = algo._h_wrapped
    assert h_before is h_after, (
        'AStarRepMOSPP should reuse the same wrapped h across '
        'sub-searches (the goal is fixed)')


# ──────────────────────────────────────────────────
#  9. Cost parity on canonical MOSPP grid
# ──────────────────────────────────────────────────


def test_kxastar_mospp_canonical_costs() -> None:
    """
    ========================================================================
     On the canonical MOSPP grid (starts=corners, goal=origin),
     per-start costs are 7 / 3 / 6 — same numerical pattern
     as the OMSPP twin by graph symmetry.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    algo = AStarRepMOSPP(problem=p, h=_manhattan_grid)
    sols = algo.run()
    costs = {(s.key.row, s.key.col): v.cost
             for s, v in sols.items()}
    assert costs == {(0, 3): 7.0, (3, 0): 3.0, (3, 3): 6.0}
