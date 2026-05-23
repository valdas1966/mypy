"""
============================================================================
 AStarIncMOSPP — ExtendableMOSPP tests.

 Covers the `extend(new_starts)` path distinct from the
 lifecycle (`_tester.py`), per-config counter
 (`_tester_counters.py`) and event-stream
 (`_tester_recording.py`) suites:
   - ExtendableMOSPP protocol satisfaction
   - extend() preconditions (run-first, non-empty)
   - run([prefix]) + extend([rest]) == fresh run([full])
     under order_starts='given' — costs AND full counters
   - the goal-anchored cache survives an extend
   - chained extend() calls; run_nested convenience
   - _repush_last_reached_start is structurally inert
============================================================================
"""

import pytest

from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.algo.i_1_mospp.mixins.extendable import (
    ExtendableMOSPP,
    is_extendable,
)
from f_hs.problem.i_0_base._factory import _ProblemGraph


def _line_problem(start_keys: list[str], goal_key: str
                  ) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C -> D -> E -> F line graph with a configurable
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


def test_astar_inc_mospp_is_extendable() -> None:
    """
    ========================================================================
     AStarIncMOSPP satisfies the ExtendableMOSPP protocol.
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical()
    assert isinstance(algo, ExtendableMOSPP)
    assert is_extendable(algo)
    assert callable(algo.extend)


# ──────────────────────────────────────────────────
#  2. Preconditions
# ──────────────────────────────────────────────────


def test_extend_before_run_raises() -> None:
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = AStarIncMOSPP(problem=p, h=_pos_h(_LINE_POS),
                         order_starts='given')
    with pytest.raises(RuntimeError):
        algo.extend([p._states['C']])


def test_extend_empty_starts_raises() -> None:
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = AStarIncMOSPP(problem=p, h=_pos_h(_LINE_POS),
                         order_starts='given')
    algo.run()
    with pytest.raises(ValueError):
        algo.extend([])


# ──────────────────────────────────────────────────
#  3. Extended run == fresh run, under order_starts='given'
# ──────────────────────────────────────────────────


def test_extend_equals_fresh_given() -> None:
    """
    ========================================================================
     Under order_starts='given', run([A, B]) + extend([C, D])
     is identical to a fresh run([A, B, C, D]) — same
     per-start costs AND the same full counter dict
     (cnt_* + mem_*). Problem order is the policy under which
     extension is metric-faithful: the new batch is appended,
     not interleaved, so it must match the fresh order too.
    ========================================================================
    """
    base = AStarIncMOSPP(
        problem=_line_problem(['A', 'B', 'C', 'D'], 'F'),
        h=_pos_h(_LINE_POS), order_starts='given')
    base.run()

    p_inc = _line_problem(['A', 'B'], 'F')
    algo = AStarIncMOSPP(problem=p_inc, h=_pos_h(_LINE_POS),
                         order_starts='given')
    algo.run()
    algo.extend([p_inc._states['C'], p_inc._states['D']])

    assert ({s.key: v.cost
             for s, v in algo.solutions.items()}
            == {s.key: v.cost
                for s, v in base.solutions.items()}
            == {'A': 5, 'B': 4, 'C': 3, 'D': 2})
    assert dict(algo.counters) == dict(base.counters)


# ──────────────────────────────────────────────────
#  4. The goal-anchored cache survives an extend
# ──────────────────────────────────────────────────


def test_extend_carries_cache() -> None:
    """
    ========================================================================
     run([A]) caches the whole A -> F on-path suffix; the
     subsequent extend([B]) finds B in the carried cache and
     terminates as a cache-hit-at-init (the headline
     incremental win, preserved across the extend boundary).
    ========================================================================
    """
    p = _line_problem(start_keys=['A'], goal_key='F')
    algo = AStarIncMOSPP(problem=p, h=_pos_h(_LINE_POS),
                         order_starts='given')
    algo.run()
    assert algo.counters['cnt_cache_hits_at_init'] == 0
    algo.extend([p._states['B']])
    assert algo.counters['cnt_cache_hits_at_init'] == 1
    assert {s.key: v.cost
            for s, v in algo.solutions.items()} == {
                'A': 5, 'B': 4}


# ──────────────────────────────────────────────────
#  5. Chained extend + run_nested
# ──────────────────────────────────────────────────


def test_extend_chain_three_calls() -> None:
    """
    ========================================================================
     run([A]) -> extend([B]) -> extend([C]) -> extend([D]).
     Final Mapping spans all starts; costs match single-shot.
    ========================================================================
    """
    p = _line_problem(start_keys=['A'], goal_key='F')
    algo = AStarIncMOSPP(problem=p, h=_pos_h(_LINE_POS),
                         order_starts='given')
    algo.run()
    algo.extend([p._states['B']])
    algo.extend([p._states['C']])
    final = algo.extend([p._states['D']])
    assert {s.key: v.cost for s, v in final.items()} == {
        'A': 5, 'B': 4, 'C': 3, 'D': 2}


def test_run_nested_astar_inc_mospp() -> None:
    """
    ========================================================================
     AStarIncMOSPP.run_nested([P1, P2, P3]) solves a
     prefix-extending sequence of MOSPP problems sharing one
     fixed goal.
    ========================================================================
    """
    p1 = _line_problem(['A'], 'F')
    p2 = _line_problem(['A', 'B'], 'F')
    p3 = _line_problem(['A', 'B', 'C'], 'F')
    algo = AStarIncMOSPP.run_nested(
        problems=[p1, p2, p3], h=_pos_h(_LINE_POS))
    assert {s.key: v.cost
            for s, v in algo.solutions.items()} == {
                'A': 5, 'B': 4, 'C': 3}


# ──────────────────────────────────────────────────
#  6. _repush is structurally inert
# ──────────────────────────────────────────────────


def test_repush_is_inert() -> None:
    """
    ========================================================================
     AStarIncMOSPP._repush_last_reached_start is a no-op (no
     shared frontier); it clears the bookkeeping.
    ========================================================================
    """
    p = _line_problem(start_keys=['A', 'B'], goal_key='F')
    algo = AStarIncMOSPP(problem=p, h=_pos_h(_LINE_POS),
                         order_starts='given')
    algo.run()
    algo._repush_last_reached_start()
    assert algo._last_reached_start is None
    assert algo._last_algo is None
