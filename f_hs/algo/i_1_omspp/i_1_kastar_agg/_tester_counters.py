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

 Distinguishing counter signatures per config:

  - `is_lazy=False` → `cnt_pop=14`, `cnt_pop_stale=0`,
                      `cnt_push=20` (14 first-time + 6 bulk
                      re-pushes from `_refresh_priorities`).
  - `is_lazy=True`  → `cnt_pop=16` (14 + 2 stale-re-pop),
                      `cnt_pop_stale=2`,
                      `cnt_push=16` (14 + 2 stale re-push).

  - `is_opt=True`  → `cnt_phi_update` and `cnt_h_update`
                     drop sharply (responsible-goal short-
                     circuit skips most refresh recomputes).
  - `is_opt=False` → every refresh recomputes F for every
                     OPEN state.

  - `store_vector=True`  → `cnt_h_update == 0` always (h
                           cached at first encounter; refresh
                           reuses cache); `cnt_h_search`
                           drops by 2 (no recompute on the
                           two `decrease_g` events).
  - `store_vector=False` → every `_compute_F` recomputes h's.

 Counters invariant across all 8 configs: `cnt_phi_search=16`
 (= `cnt_generated=14` first-time pushes + `cnt_decrease=2`
 decrease_g events), `cnt_expanded=14`, `cnt_generated=14`,
 `cnt_decrease=2`.
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
     - `cnt_push=20` = 14 first-time + 6 bulk re-pushes
       (2 eager refreshes × 3 OPEN states each).
     - `cnt_phi_update=6` = every OPEN state recomputed at
       each refresh (no opt short-circuit).
     - `cnt_h_update=9` = h-recomputes during the 6 refresh
       recomputes (active goals shrink as goals are found,
       so per-call counts vary: 2 + 2 + 1 + 1 + 1 + 1 + ...
       summing to 9).
     - `cnt_h_search=34` = sum over the 16 search-phase
       _compute_F calls of (#active goals at call time).
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    9,
        'cnt_phi_search': 16,
        'cnt_phi_update':  6,
        'cnt_push':       20,
        'cnt_pop':        14,
        'cnt_pop_stale':   0,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
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
     - `cnt_h_search=32` — vector built ONCE per state at
       first encounter (n_active at that moment); subsequent
       `_compute_F` calls (incl. the 2 decrease_g events)
       reuse the cache. Drops by 2 from nosv (the 2
       decrease_g events would have re-computed h's).
     - All other counters identical to eager_noopt_nosv.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   32,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  6,
        'cnt_push':       20,
        'cnt_pop':        14,
        'cnt_pop_stale':   0,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_eager_opt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=True,
     store_vector=False.

     Distinguishing values:
     - `cnt_phi_update=3` (was 6 in noopt) — `_refresh_priorities`
       skips F-recompute for OPEN states whose responsible
       goal is not the just-removed one. Half the refresh
       work disappears.
     - `cnt_h_update=4` (was 9 in noopt) — fewer h calls
       inside the smaller set of refresh recomputes.
     - `cnt_h_search=34` — search-phase h calls also include
       `_compute_F`'s argmin pass that assigns
       `_responsible[state]` (already counted as part of the
       per-active-goal h sweep).
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=True,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    4,
        'cnt_phi_search': 16,
        'cnt_phi_update':  3,
        'cnt_push':       20,
        'cnt_pop':        14,
        'cnt_pop_stale':   0,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_eager_opt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=False, is_opt=True,
     store_vector=True. Pareto-optimal eager config.

     Distinguishing values:
     - `cnt_h_update=0` (vector cached) AND `cnt_phi_update=3`
       (opt skip) — both refresh-side optimisations active.
     - `cnt_h_search=32` (vector saves the 2 decrease_g
       recomputes) and identical eager push/pop pattern.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=True,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   32,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  3,
        'cnt_push':       20,
        'cnt_pop':        14,
        'cnt_pop_stale':   0,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
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
     - `cnt_pop=16` = 14 real pops + 2 stale re-pops.
     - `cnt_pop_stale=2`, `cnt_push=16` (14 first-time + 2
       stale re-push; bulk-refresh path is dead in lazy mode).
     - `cnt_phi_update=16` — every pop re-checks F (no opt
       short-circuit), one `_compute_F` per pop.
     - `cnt_h_update=31` — sum over the 16 update-phase
       `_compute_F` calls of #active goals at that moment.
       Active set shrinks 3 → 2 → 1 across the run, so the
       per-call cost decays.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':   31,
        'cnt_phi_search': 16,
        'cnt_phi_update': 16,
        'cnt_push':       16,
        'cnt_pop':        16,
        'cnt_pop_stale':   2,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
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
     - `cnt_h_search=32` — same drop-by-2 vs nosv as in eager.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   32,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update': 16,
        'cnt_push':       16,
        'cnt_pop':        16,
        'cnt_pop_stale':   2,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_lazy_opt_nosv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=True,
     store_vector=False.

     Distinguishing values:
     - `cnt_phi_update=2` (was 16 in noopt) — opt skips
       pop-time recompute whenever the popped state's
       responsible goal is still active. Only 2 pops actually
       hit the recompute path (those whose responsible goal
       was already closed).
     - `cnt_h_update=3` — h calls within those 2 recomputes.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    3,
        'cnt_phi_search': 16,
        'cnt_phi_update':  2,
        'cnt_push':       16,
        'cnt_pop':        16,
        'cnt_pop_stale':   2,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
        'cnt_generated':  14,
    }


def test_counters_canonical_omspp_min_lazy_opt_sv() -> None:
    """
    ========================================================================
     Pin KAStarAgg-MIN counters: is_lazy=True, is_opt=True,
     store_vector=True. Pareto-optimal lazy config.

     Distinguishing values:
     - `cnt_h_update=0` (cache) AND `cnt_phi_update=2`
       (opt skip) — minimal refresh-side work.
     - `cnt_h_search=32` (cache) — search-side savings.
     - Heap-ops: `cnt_pop=16`, `cnt_push=16` — same as
       lazy_*_nosv (h-cache doesn't change heap activity).
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   32,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  2,
        'cnt_push':       16,
        'cnt_pop':        16,
        'cnt_pop_stale':   2,
        'cnt_decrease':    2,
        'cnt_expanded':   14,
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
     contract of KAStarAgg.
    ========================================================================
    """
    algo = _make_algo(is_lazy=is_lazy, is_opt=is_opt,
                      store_vector=store_vector)
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7, (3, 0): 3, (3, 3): 6}
