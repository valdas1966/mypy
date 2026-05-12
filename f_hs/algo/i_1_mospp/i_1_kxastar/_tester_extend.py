import pytest

from f_hs.algo.i_1_mospp.i_1_kxastar import KxAStarMOSPP
from f_hs.algo.i_1_mospp.mixins.extendable import (
    ExtendableMOSPP,
    is_extendable,
)
from f_hs.problem.i_0_base._factory import _ProblemGraph


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


# ──────────────────────────────────────────────────
#  1. Capability
# ──────────────────────────────────────────────────


def test_kxastar_mospp_is_extendable() -> None:
    """
    ========================================================================
     KxAStarMOSPP satisfies the ExtendableMOSPP protocol.
    ========================================================================
    """
    algo = KxAStarMOSPP.Factory.graph_abc_two_starts()
    assert isinstance(algo, ExtendableMOSPP)
    assert is_extendable(algo)
    assert callable(algo.extend)


# ──────────────────────────────────────────────────
#  2. Preconditions
# ──────────────────────────────────────────────────


def test_extend_before_run_raises() -> None:
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS))
    with pytest.raises(RuntimeError):
        algo.extend([p._states['C']])


def test_extend_empty_starts_raises() -> None:
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    with pytest.raises(ValueError):
        algo.extend([])


# ──────────────────────────────────────────────────
#  3. Baseline parity vs single-shot
# ──────────────────────────────────────────────────


def test_extend_matches_single_shot() -> None:
    """
    ========================================================================
     run([A, B]) + extend([C, D]) yields the same per-start
     costs as a single-shot run([A, B, C, D]).
    ========================================================================
    """
    p_full = _line_problem(
        start_keys=['A', 'B', 'C', 'D'], goal_key='F')
    baseline = KxAStarMOSPP(problem=p_full,
                            h=_pos_h(_LINE_POS))
    sol_full = baseline.run()
    base_costs = {s.key: v.cost for s, v in sol_full.items()}

    p_inc = _line_problem(
        start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p_inc, h=_pos_h(_LINE_POS))
    algo.run()
    sol_ext = algo.extend(
        [p_inc._states['C'], p_inc._states['D']])
    ext_costs = {s.key: v.cost for s, v in sol_ext.items()}
    assert ext_costs == base_costs
    assert ext_costs == {'A': 5, 'B': 4, 'C': 3, 'D': 2}


# ──────────────────────────────────────────────────
#  4. Already_reached fast-path skip via extend
# ──────────────────────────────────────────────────


def test_extend_skips_already_solved_start() -> None:
    """
    ========================================================================
     Re-submitting a solved start hits already_reached: NO
     new A* runs.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_recording=True)
    algo.run()
    expanded_before = algo.counters['cnt_expanded']

    sol2 = algo.extend([p._states['A']])
    by_key = {s.key: v for s, v in sol2.items()}
    assert by_key['A'].cost == 5
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    assert on_starts[-1]['reason'] == 'already_reached'
    assert algo.counters['cnt_expanded'] == expanded_before


# ──────────────────────────────────────────────────
#  5. Sequence chain
# ──────────────────────────────────────────────────


def test_extend_chain_three_calls() -> None:
    """
    ========================================================================
     run([A]) → extend([B]) → extend([C]) → extend([D]).
     Final Mapping spans all starts; costs match single-shot.
    ========================================================================
    """
    p = _line_problem(start_keys=['A'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    algo.extend([p._states['B']])
    algo.extend([p._states['C']])
    final = algo.extend([p._states['D']])
    costs = {s.key: v.cost for s, v in final.items()}
    assert costs == {'A': 5, 'B': 4, 'C': 3, 'D': 2}


# ──────────────────────────────────────────────────
#  6. Counter accumulation
# ──────────────────────────────────────────────────


def test_extend_counters_cumulative() -> None:
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    before = dict(algo.counters)
    algo.extend([p._states['C']])
    after = dict(algo.counters)
    for k in ('cnt_h_search', 'cnt_push', 'cnt_pop',
              'cnt_expanded', 'cnt_generated'):
        assert after[k] >= before[k]


# ──────────────────────────────────────────────────
#  7. _repush is structurally inert
# ──────────────────────────────────────────────────


def test_repush_is_inert() -> None:
    """
    ========================================================================
     kxA*-MOSPP's _repush_last_reached_start is a no-op
     (no shared frontier). Bookkeeping cleared after the call.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = KxAStarMOSPP(problem=p, h=_pos_h(_LINE_POS),
                        is_recording=True)
    algo.run()
    pushes_before = sum(1 for e in algo.recorder.events
                        if e['type'] == 'push')
    algo._repush_last_reached_start()
    pushes_after = sum(1 for e in algo.recorder.events
                       if e['type'] == 'push')
    assert pushes_after == pushes_before
    assert algo._last_reached_start is None
    assert algo._last_algo is None


# ──────────────────────────────────────────────────
#  8. run_nested convenience
# ──────────────────────────────────────────────────


def test_run_nested_kxastar_mospp() -> None:
    """
    ========================================================================
     KxAStarMOSPP.run_nested([P1, P2, P3]) solves a
     prefix-extending sequence of MOSPP problems.
    ========================================================================
    """
    p1 = _line_problem(start_keys=['A'], goal_key='F')
    p2 = _line_problem(start_keys=['A', 'B'], goal_key='F')
    p3 = _line_problem(start_keys=['A', 'B', 'C'],
                       goal_key='F')
    algo = KxAStarMOSPP.run_nested(
        problems=[p1, p2, p3], h=_pos_h(_LINE_POS))
    by_key = {s.key: v.cost
              for s, v in algo.solutions.items()}
    assert by_key == {'A': 5, 'B': 4, 'C': 3}
