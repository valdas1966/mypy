"""
============================================================================
 KAStarAgg — counter pins on the canonical OMSPP problem
 (`Factory.grid_4x4_obstacle_omspp`: start (0,0), goals
 (0,3) / (3,0) / (3,3); per-goal optimal costs 7 / 3 / 6;
 Manhattan h to each goal). Aggregator: MIN.

 One test per param-config (8 total = 2³ combinations of
 `is_lazy` × `is_opt` × `store_vector`). Each pins the FULL
 10-counter dict (memory snapshots excluded — they're env-
 dependent). A single invariant-costs test verifies that the
 8 configs all produce identical optimal per-goal costs.

 Goal-handling: lazy re-push (INC-symmetric). The just-found
 non-last goal is re-pushed instead of force-expanded; its
 successors are reached via other paths during the search.
 The last active goal is NEVER re-pushed.

 Distinguishing counter signatures per config:

  - `is_lazy=False` → `cnt_pop=12`, `cnt_pop_stale=0`,
                      `cnt_push=24` (14 first-time + 2 goal
                      re-pushes + 8 bulk re-pushes from
                      `_refresh_priorities`: 3 OPEN states
                      after (3,0)-find + 5 OPEN states after
                      (3,3)-find).
  - `is_lazy=True`  → `cnt_pop=16` (12 emitted + 4 stale-re-pop),
                      `cnt_pop_stale=4`,
                      `cnt_push=20` (14 first-time + 2 goal
                      re-pushes + 4 stale re-pushes).

  - `is_opt=True`  → `cnt_phi_update` and `cnt_h_update`
                     drop sharply (responsible-goal short-
                     circuit skips most refresh / pop-time
                     recomputes).
  - `is_opt=False` → every refresh / lazy-pop recomputes F.

  - `store_vector=True`  → `cnt_h_update == 0` always (h
                           cached at first encounter; refresh
                           and goal re-push reuse cache);
                           `cnt_h_search` drops by 3 (the 2
                           goal re-pushes' h-calls and 1 from
                           the smaller eager refresh path
                           collapse to cache reads).
  - `store_vector=False` → every `_compute_F` recomputes h's.

 Counters invariant across all 8 configs (under the new
 lazy-re-push design):

   `cnt_phi_search=16` — 14 first-time pushes + 2 goal
                         re-pushes. Both _compute_F at
                         PHASE_SEARCH.
   `cnt_decrease=0`    — no decrease-key races. (2,2)/(2,3)
                         are first-pushed at their optimal g
                         via (2,1)/(2,2) (no detour through
                         goals).
   `cnt_expanded=9`    — 9 non-goal expansions. The 3 goals
                         are NOT expanded at goal-find (lazy
                         re-push design); none of them re-pop
                         before `active_goals` empties on this
                         canonical, so they never enter the
                         expansion path.
   `cnt_generated=14`  — same set of unique states reached.
============================================================================
"""

import pytest

from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_1_grid import ProblemGrid


def _make_algo(is_lazy: bool,
               is_opt: bool,
               store_vector: bool) -> KAStarAgg:
    """
    ========================================================================
     Build a KAStarAgg-MIN on the canonical OMSPP problem
     for the given (is_lazy, is_opt, store_vector) config.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle_omspp()
    return KAStarAgg(problem=p,
                     h=lambda s, g: float(s.distance(g)),
                     agg='MIN',
                     is_lazy=is_lazy,
                     is_opt=is_opt,
                     store_vector=store_vector)


def _run_and_strip_mem(algo: KAStarAgg) -> dict[str, int]:
    """
    ========================================================================
     Run the algo and return the counter dict with memory
     snapshots stripped (env-dependent).
    ========================================================================
    """
    algo.run()
    return {k: v for k, v in algo.counters.items()
            if not k.startswith('mem_')}


# ──────────────────────────────────────────────────────────
#  Eager — is_lazy=False (bulk refresh after each goal-find)
# ──────────────────────────────────────────────────────────


def test_counters_canonical_omspp_min_eager_noopt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=False,
     store_vector=False.

     Distinguishing values:
     - `cnt_push=24` = 14 first-time + 2 goal re-pushes
       ((3,0), (3,3)) + 8 bulk re-pushes (3 + 5 across the
       two refreshes).
     - `cnt_phi_update=8` = 3 (refresh after (3,0)) + 5
       (refresh after (3,3)) — every OPEN state recomputed
       at each refresh (no opt short-circuit).
     - `cnt_h_update=11` = 6 (3 states × 2 active in refresh
       1) + 5 (5 states × 1 active in refresh 2).
     - `cnt_h_search=37` = sum over 16 search-phase
       _compute_F calls of (#active goals at call time).
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   37,
        'cnt_h_update':   11,
        'cnt_phi_search': 16,
        'cnt_phi_update':  8,
        'cnt_push':       24,
        'cnt_pop':        12,
        'cnt_pop_stale':   0,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_eager_noopt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=False,
     store_vector=True.

     Distinguishing values:
     - `cnt_h_update=0` — refresh reuses cached vectors; h
       is never recomputed in update flow.
     - `cnt_h_search=34` — vector built ONCE per state at
       first encounter (n_active at that moment); the 2 goal
       re-pushes reuse the cached vectors. Drops by 3 from
       nosv (the 2 + 1 h-calls the goal re-pushes would have
       performed).
     - All other counters identical to eager_noopt_nosv.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  8,
        'cnt_push':       24,
        'cnt_pop':        12,
        'cnt_pop_stale':   0,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_eager_opt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=True,
     store_vector=False.

     Distinguishing values:
     - `cnt_phi_update=4` (was 8 in noopt) — `_refresh_priorities`
       skips F-recompute for OPEN states whose responsible
       goal is not the just-removed one. 1 recompute in
       refresh 1 (only (2,1) had responsible=(3,0)) + 3
       recomputes in refresh 2 (states whose responsible was
       (3,3) — (3,0) re-pushed, (3,1), (3,2)).
     - `cnt_h_update=5` = 2 (refresh 1, 1 state × 2 active)
       + 3 (refresh 2, 3 states × 1 active).
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=True,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   37,
        'cnt_h_update':    5,
        'cnt_phi_search': 16,
        'cnt_phi_update':  4,
        'cnt_push':       24,
        'cnt_pop':        12,
        'cnt_pop_stale':   0,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_eager_opt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=True,
     store_vector=True. Pareto-optimal eager config.

     Distinguishing values:
     - `cnt_h_update=0` (vector cached) AND `cnt_phi_update=4`
       (opt skip) — both refresh-side optimisations active.
     - `cnt_h_search=34` (vector saves the 3 goal re-push
       h-calls) and identical eager push/pop pattern.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=True,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  4,
        'cnt_push':       24,
        'cnt_pop':        12,
        'cnt_pop_stale':   0,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


# ──────────────────────────────────────────────────────────
#  Lazy — is_lazy=True (refresh deferred to pop time)
# ──────────────────────────────────────────────────────────


def test_counters_canonical_omspp_min_lazy_noopt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=False,
     store_vector=False.

     Distinguishing values:
     - `cnt_pop=16` = 12 emitted + 4 stale re-pops ((2,1)
       once after (3,0)-find; (3,0)/(3,1)/(3,2) each once
       after (3,3)-find).
     - `cnt_pop_stale=4`, `cnt_push=20` (14 first-time + 2
       goal re-pushes + 4 stale re-pushes; bulk-refresh path
       is dead in lazy mode).
     - `cnt_phi_update=16` — every pop re-checks F (no opt
       short-circuit), one `_compute_F` per pop.
     - `cnt_h_update=32` — sum over the 16 update-phase
       `_compute_F` calls of #active goals at that moment.
       Active set shrinks 3 → 2 → 1 across the run.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   37,
        'cnt_h_update':   32,
        'cnt_phi_search': 16,
        'cnt_phi_update': 16,
        'cnt_push':       20,
        'cnt_pop':        16,
        'cnt_pop_stale':   4,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_lazy_noopt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=False,
     store_vector=True.

     Distinguishing values:
     - `cnt_h_update=0` — vector cache. `cnt_phi_update=16`
       still fires (recompute-Φ-from-cache happens at every
       pop) but no h calls.
     - `cnt_h_search=34` — same drop-by-3 vs nosv as in eager.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update': 16,
        'cnt_push':       20,
        'cnt_pop':        16,
        'cnt_pop_stale':   4,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_lazy_opt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=True,
     store_vector=False.

     Distinguishing values:
     - `cnt_phi_update=4` (was 16 in noopt) — opt skips
       pop-time recompute whenever the popped state's
       responsible goal is still active. Only 4 pops actually
       hit the recompute path (the 4 stale pops, whose
       responsible was the just-removed goal).
     - `cnt_h_update=5` — h calls within those 4 recomputes.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   37,
        'cnt_h_update':    5,
        'cnt_phi_search': 16,
        'cnt_phi_update':  4,
        'cnt_push':       20,
        'cnt_pop':        16,
        'cnt_pop_stale':   4,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_lazy_opt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=True,
     store_vector=True. Pareto-optimal lazy config.

     Distinguishing values:
     - `cnt_h_update=0` (cache) AND `cnt_phi_update=4`
       (opt skip) — minimal refresh-side work.
     - `cnt_h_search=34` (cache) — search-side savings.
     - Heap-ops: `cnt_pop=16`, `cnt_push=20` — same as
       lazy_*_nosv (h-cache doesn't change heap activity).
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  4,
        'cnt_push':       20,
        'cnt_pop':        16,
        'cnt_pop_stale':   4,
        'cnt_decrease':    0,
        'cnt_expanded':    9,
        'cnt_generated':  14,
    }


# ──────────────────────────────────────────────────────────
#  Cross-config invariants
# ──────────────────────────────────────────────────────────


@pytest.mark.parametrize('is_lazy', [False, True])
@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_per_goal_costs_invariant_across_configs(
        is_lazy: bool,
        is_opt: bool,
        store_vector: bool) -> None:
    """
    ========================================================================
     Per-goal optimal costs are invariant across all 8
     param-configs: (0,3)=7, (3,0)=3, (3,3)=6.

     Different configs trade off counter values but must
     never differ on optimal cost — that's the soundness
     contract of KAStarAgg. Crucially, the lazy-re-push
     design preserves this: under consistent h with MIN
     aggregation, a goal whose optimal path passes through
     another goal will see that other goal re-pop at
     f_new ≤ C* before it is found.
    ========================================================================
    """
    algo = _make_algo(is_lazy=is_lazy, is_opt=is_opt,
                      store_vector=store_vector)
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7, (3, 0): 3, (3, 3): 6}
