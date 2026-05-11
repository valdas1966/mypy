"""
============================================================================
 KAStarAgg — full event-stream pins on the canonical OMSPP
 problem (`Factory.grid_4x4_obstacle_omspp`: start (0,0),
 goals (0,3) / (3,0) / (3,3); per-goal optimal costs 7 / 3 / 6;
 Manhattan h to each goal). Aggregator: MIN.

 Minimal INC-aligned schema: 5 event types (`push`, `pop`,
 `decrease_g`, `on_goal`, `update_frontier`). The recording
 stream is INVARIANT to (`is_opt`, `store_vector`) — those
 params affect only counters (`cnt_h_*`, `cnt_phi_*`,
 `cnt_pop_stale`), not the event sequence. Only `is_lazy`
 distinguishes the streams:

   - `is_lazy=False` → 33 events (incl. 2 `update_frontier`
                       boundary markers, one per non-final
                       goal-find).
   - `is_lazy=True`  → 31 events (no `update_frontier`; lazy
                       refresh is silent).

 Goal-handling order at every goal-find (INC-symmetric lazy
 re-push):

     pop  → on_goal  → push (re-push, if non-last)
                     → update_frontier (eager only)

 The just-found goal is NOT force-expanded; its successors
 are reached via other paths during the search. The two
 pinned streams below define the canonical eager and lazy
 event sequences. A parametrized invariance check then
 asserts every (is_opt × store_vector) combination produces
 identical events to the canonical for that `is_lazy`.

 If a future change makes opt or store_vector observable in
 the event stream, the invariance check will fail at the
 deviating cell — surfacing the schema drift directly.
============================================================================
"""

import pytest

from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_1_grid import ProblemGrid


def _make_algo(is_lazy: bool,
               is_opt: bool,
               store_vector: bool) -> KAStarAgg:
    """
    ========================================================================
     Build a KAStarAgg-MIN on the canonical OMSPP problem
     for the given config, with recording enabled.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    return KAStarAgg(problem=p,
                     h=lambda s, g: float(s.distance(g)),
                     agg='MIN',
                     is_lazy=is_lazy,
                     is_opt=is_opt,
                     store_vector=store_vector,
                     is_recording=True)


def _events_of(algo: KAStarAgg) -> list[dict]:
    """
    ========================================================================
     Run the algo and return its normalized event list.
    ========================================================================
    """
    algo.run()
    return [normalize(e) for e in algo.recorder.events]


# ──────────────────────────────────────────────────────────
#  Canonical streams (one per `is_lazy` value)
# ──────────────────────────────────────────────────────────


_EAGER_CANONICAL: list[dict] = [
    {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
    {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
    {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
    {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
    {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
    {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
    {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 2, 'f': 3},
    {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 1, 'f': 3, 'parent': (1, 0)},
    {'type': 'pop', 'state': (2, 0), 'g': 2, 'h': 1, 'f': 3},
    {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 2, 'f': 5, 'parent': (2, 0)},
    {'type': 'push', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3, 'parent': (2, 0)},
    {'type': 'pop', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3},
    {'type': 'on_goal', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'goal_index': 1},
    {'type': 'push', 'state': (3, 0), 'g': 3, 'h': 3, 'f': 6, 'parent': (2, 0)},
    {'type': 'update_frontier', 'num_nodes': 3, 'next_goal_index': 0},
    {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
    {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
    {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
    {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
    {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
    {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
    {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
    {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
    {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
    {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
    {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
    {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 2},
    {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 3, 'f': 9, 'parent': (2, 3)},
    {'type': 'update_frontier', 'num_nodes': 5, 'next_goal_index': 0},
    {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
    {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
    {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
]


_LAZY_CANONICAL: list[dict] = [
    {'type': 'push', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3, 'parent': None},
    {'type': 'pop', 'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
    {'type': 'push', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
    {'type': 'push', 'state': (1, 0), 'g': 1, 'h': 2, 'f': 3, 'parent': (0, 0)},
    {'type': 'pop', 'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
    {'type': 'push', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5, 'parent': (0, 1)},
    {'type': 'pop', 'state': (1, 0), 'g': 1, 'h': 2, 'f': 3},
    {'type': 'push', 'state': (2, 0), 'g': 2, 'h': 1, 'f': 3, 'parent': (1, 0)},
    {'type': 'pop', 'state': (2, 0), 'g': 2, 'h': 1, 'f': 3},
    {'type': 'push', 'state': (2, 1), 'g': 3, 'h': 2, 'f': 5, 'parent': (2, 0)},
    {'type': 'push', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3, 'parent': (2, 0)},
    {'type': 'pop', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3},
    {'type': 'on_goal', 'state': (3, 0), 'g': 3, 'reason': 'expanded', 'goal_index': 1},
    # Lazy goal re-push (2026-05-11 skip): emitted with the
    # STALE F (= popped F = g for MIN). The next pop of this
    # entry is a silent stale-pop that refreshes F to g + min
    # h to remaining active goals.
    {'type': 'push', 'state': (3, 0), 'g': 3, 'h': 0, 'f': 3, 'parent': (2, 0)},
    {'type': 'pop', 'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
    {'type': 'pop', 'state': (2, 1), 'g': 3, 'h': 3, 'f': 6},
    {'type': 'push', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
    {'type': 'push', 'state': (3, 1), 'g': 4, 'h': 2, 'f': 6, 'parent': (2, 1)},
    {'type': 'pop', 'state': (2, 2), 'g': 4, 'h': 2, 'f': 6},
    {'type': 'push', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
    {'type': 'push', 'state': (3, 2), 'g': 5, 'h': 1, 'f': 6, 'parent': (2, 2)},
    {'type': 'pop', 'state': (2, 3), 'g': 5, 'h': 1, 'f': 6},
    {'type': 'push', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7, 'parent': (2, 3)},
    {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
    {'type': 'pop', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6},
    {'type': 'on_goal', 'state': (3, 3), 'g': 6, 'reason': 'expanded', 'goal_index': 2},
    # Lazy goal re-push (2026-05-11 skip): stale F.
    {'type': 'push', 'state': (3, 3), 'g': 6, 'h': 0, 'f': 6, 'parent': (2, 3)},
    {'type': 'pop', 'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
    {'type': 'push', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7, 'parent': (1, 3)},
    {'type': 'pop', 'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    {'type': 'on_goal', 'state': (0, 3), 'g': 7, 'reason': 'expanded', 'goal_index': 0},
]


# ──────────────────────────────────────────────────────────
#  Canonical-stream pins
# ──────────────────────────────────────────────────────────


def test_recording_canonical_omspp_min_eager() -> None:
    """
    ========================================================================
     Pin the canonical eager event stream (33 events) on the
     canonical OMSPP problem with KAStarAgg-MIN, is_lazy=False.

     Distinguishing eager features:
     - 2 `update_frontier` boundary markers (one per non-
       final goal-find: index 1 → 0, then index 2 → 0).
     - At each goal-find: `pop` → `on_goal` → `push` (re-push,
       INC-symmetric) → `update_frontier`.
     - All 12 emitted pops are real expansions or goal-finds
       (no stale pops in eager mode).
     - 14 first-encounter pushes + 2 goal re-pushes
       ((3,0) and (3,3); (0,3) is last and not re-pushed).
     - 0 `decrease_g` events — under proposal, (2,2) and
       (2,3) are first-pushed at their optimal g (via (2,1)
       and (2,2)), so no decrease-key race.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=False)
    assert _events_of(algo) == _EAGER_CANONICAL


def test_recording_canonical_omspp_min_lazy() -> None:
    """
    ========================================================================
     Pin the canonical lazy event stream (31 events) on the
     canonical OMSPP problem with KAStarAgg-MIN, is_lazy=True.

     Distinguishing lazy features:
     - No `update_frontier` markers (refresh is inline at
       pop time, no between-phase moment).
     - The 4 stale pops are silent in the stream — `pop`
       events fire only for real expansions, so the visible
       pop count matches eager (12).
     - Identical to `_EAGER_CANONICAL` apart from the 2
       missing `update_frontier` events.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=False)
    assert _events_of(algo) == _LAZY_CANONICAL


# ──────────────────────────────────────────────────────────
#  Cross-config invariance: opt × store_vector don't perturb
#  the recording stream.
# ──────────────────────────────────────────────────────────


@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_recording_invariant_eager_across_opt_sv(
        is_opt: bool, store_vector: bool) -> None:
    """
    ========================================================================
     Under is_lazy=False, the event stream is invariant to
     (is_opt, store_vector). Both parameters affect only
     counters, never the kept events.

     Asserts the full stream equals `_EAGER_CANONICAL` for
     every (opt × sv) cell. A regression that surfaces opt
     or store_vector in events would fail at the deviating
     cell, identifying the schema drift directly.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=is_opt,
                      store_vector=store_vector)
    assert _events_of(algo) == _EAGER_CANONICAL


@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_recording_invariant_lazy_across_opt_sv(
        is_opt: bool, store_vector: bool) -> None:
    """
    ========================================================================
     Under is_lazy=True, the event stream is invariant to
     (is_opt, store_vector). The opt short-circuit and the
     vector cache only affect counters; the kept events are
     identical across all four (opt × sv) cells.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=is_opt,
                      store_vector=store_vector)
    assert _events_of(algo) == _LAZY_CANONICAL
