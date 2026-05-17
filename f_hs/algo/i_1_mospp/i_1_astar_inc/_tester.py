"""
============================================================================
 AStarIncMOSPP — lifecycle tests.

 Smoke / contract coverage distinct from the per-config
 counter (`_tester_counters.py`) and event-stream
 (`_tester_recording.py`) pins:
   - canonical correctness + cache-hit-at-init
   - construction validation (multi-goal, bad order policy)
   - duplicate-start `already_reached` fast-path
   - `order_starts` policies (all yield identical per-start
     costs — order is a perf knob, not a correctness one)
   - no PHASE_UPDATE (`elapsed_update == 0.0`)
   - `update_frontier` never emitted
   - `reconstruct_path` returns `[]`
   - carry-cache toggle changes cache-hit-at-init accounting
============================================================================
"""

import pytest

from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.problem.i_1_grid import ProblemGrid

_COSTS = {(0, 0): 15.0, (2, 3): 10.0, (0, 3): 12.0}


def _costs(algo: AStarIncMOSPP) -> dict:
    """
    ========================================================================
     `{(row, col): cost}` view of the per-start solutions.
    ========================================================================
    """
    return {(s.key.row, s.key.col): v.cost
            for s, v in algo.solutions.items()}


def test_canonical_costs_and_cache_hit_at_init() -> None:
    """
    ========================================================================
     Default config: per-start costs 15 / 10 / 12; the
     (2,3) sub-search is a cache-hit-at-init (it lies on the
     (0,0)->(5,0) cached path).
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical()
    algo.run()
    assert _costs(algo) == _COSTS
    assert algo.counters['cnt_cache_hits_at_init'] == 1


def test_multi_goal_rejected() -> None:
    """
    ========================================================================
     MOSPP requires exactly one goal — a multi-goal problem
     raises ValueError at construction.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()  # 3 goals
    with pytest.raises(ValueError):
        AStarIncMOSPP(problem=p, h=lambda s, g: 0.0)


def test_bad_order_starts_rejected() -> None:
    """
    ========================================================================
     An unknown `order_starts` policy raises ValueError.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
    with pytest.raises(ValueError):
        AStarIncMOSPP(problem=p, h=lambda s, g: 0.0,
                      order_starts='spiral')


def test_duplicate_start_already_reached() -> None:
    """
    ========================================================================
     starts=[A, A]: sub-search 1 finalizes A; sub-search 2
     hits the `already_reached` fast-path and emits its
     on_start with that reason.
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.graph_abc_repeated_start()
    algo.recorder.is_active = True
    algo.run()
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    assert len(on_starts) == 2
    assert on_starts[1]['reason'] == 'already_reached'
    assert {st.key: v.cost
            for st, v in algo.solutions.items()} == {'A': 1.0}


def test_order_policies_all_correct() -> None:
    """
    ========================================================================
     Every `order_starts` policy yields the SAME per-start
     costs — ordering changes the work, never the answer.
    ========================================================================
    """
    for policy in ('near', 'far', 'mean', 'random'):
        algo = AStarIncMOSPP.Factory.canonical(
            order_starts=policy)
        algo.run()
        assert _costs(algo) == _COSTS, policy


def test_elapsed_update_is_zero() -> None:
    """
    ========================================================================
     No PHASE_UPDATE flips in incremental MOSPP — the update
     wall-clock bucket stays 0.0.
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical()
    algo.run()
    assert algo.elapsed_update == 0.0


def test_no_update_frontier_event() -> None:
    """
    ========================================================================
     `update_frontier` is never emitted (no shared frontier
     to transition between sub-searches).
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical()
    algo.recorder.is_active = True
    algo.run()
    assert all(e['type'] != 'update_frontier'
               for e in algo.recorder.events)


def test_reconstruct_path_empty() -> None:
    """
    ========================================================================
     Sub-search parent pointers are discarded — path
     reconstruction returns `[]` (mirror of AStarRepMOSPP).
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical()
    algo.run()
    start = next(iter(algo.solutions))
    assert algo.reconstruct_path(start) == []


def test_carry_cache_off_disables_cache_hit_at_init() -> None:
    """
    ========================================================================
     With `carry_cache=False` no cache crosses sub-searches,
     so cache-hit-at-init never fires — yet costs are still
     correct (each sub-search solves from scratch).
    ========================================================================
    """
    algo = AStarIncMOSPP.Factory.canonical(carry_cache=False)
    algo.run()
    assert _costs(algo) == _COSTS
    assert algo.counters['cnt_cache_hits_at_init'] == 0
