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

 Counter taxonomy (Path D, 2026-05-11): strictly temporal —
 the counter axis mirrors the structural `phase` axis.

   `cnt_h_search`  — h-calls during PHASE_SEARCH (= inside
                     the main search loop): first-encounter,
                     decrease-g, lazy pop-time staleness
                     check, AND the eager goal re-push at
                     goal-find (which lives temporally in
                     SEARCH — the structural flip to UPDATE
                     happens around the bulk refresh).
   `cnt_h_update`  — h-calls during PHASE_UPDATE (= inside
                     `_refresh_priorities`). Eager-only.
                     **Lazy: always 0** — lazy never enters
                     PHASE_UPDATE; its active-set-change
                     response is folded into the search loop
                     via pop-time staleness checks.

 Symmetric for Φ via `cnt_phi_search` / `cnt_phi_update`.

 Lazy goal re-push skip (2026-05-11): at goal-find, lazy
 mode does NOT recompute F under the shrunken active set.
 It pushes the goal back with its STALE F (= popped F);
 the next stale-pop detects and re-pushes at the correct
 priority. Cost: +1 stale pop per non-last goal-find on top
 of the prior lazy stale-pop count. Embodies "lazy = no
 work between sub-search segments".

 Distinguishing counter signatures per config:

  - `is_lazy=False` → `cnt_pop=12` (clean pops; bulk-refresh
                      prevents stale OPEN entries from
                      existing),
                      `cnt_push=24` (14 first-time + 2 goal
                      re-pushes + 8 bulk re-pushes from
                      `_refresh_priorities`: 3 OPEN states
                      after (3,0)-find + 5 OPEN states after
                      (3,3)-find).
                      `cnt_h_update > 0` (refresh body).
  - `is_lazy=True`  → `cnt_pop=18` (12 real + 6 stale; stale
                      subset = cnt_pop − cnt_expanded − 3
                      on_goal events = 18 − 9 − 3 = 6),
                      `cnt_push=22` (14 first-time + 2 goal
                      re-pushes + 6 stale re-pushes). The 2
                      extra stale pops vs. pre-skip come from
                      the deferred goal re-pushes ((3,0) and
                      (3,3) each get one extra stale pop just
                      after being found).
                      `cnt_h_update == 0` (lazy never enters
                      PHASE_UPDATE).

  - `is_opt=True`  → `cnt_phi_update` and `cnt_h_update`
                     drop in eager (responsible-goal short-
                     circuit skips most refresh recomputes);
                     `cnt_phi_search` / `cnt_h_search` drop
                     in lazy (the staleness check skips when
                     the popped state's responsible goal is
                     still active).
  - `is_opt=False` → eager refresh recomputes every OPEN
                     state EXCEPT the just-re-pushed goal
                     (`just_re_pushed_state` short-circuit,
                     2026-05-09); lazy stale-pop check
                     recomputes every pop.

  - `store_vector=True`  → `cnt_h_search` drops to its
                           **first-encounter floor** (34 on
                           canonical) and `cnt_h_update == 0`:
                           the vector cache absorbs every
                           later h-read (lazy stale-pop, lazy
                           goal-stale-pop, eager refresh,
                           eager goal re-push). Φ-call counts
                           are unaffected.
  - `store_vector=False` → every `_compute_F` recomputes h's.

 Counters invariant across all 8 configs (under Path D +
 lazy goal-repush skip):

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

 NOTE: `cnt_h_search` is NO LONGER invariant under Path D —
 lazy modes count their pop-time staleness h-work here too,
 so lazy values are larger than eager values for the same
 sv. Eager nosv: 37 (= 34 first-encounter + 3 goal re-push).
 Eager sv: 34. Lazy varies with `is_opt` and `store_vector`.
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
                     h=lambda s, g: float(s.key.distance(g.key)),
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
     - `cnt_h_search=37` = 34 first-encounter + 3 goal re-push
       (2 active for (3,0) re-push + 1 active for (3,3) re-
       push; the eager goal re-push uses PHASE_SEARCH under
       Path D — it lives temporally inside the search loop).
     - `cnt_h_update=8` = 4 (refresh 1: 2 states × 2 active)
       + 4 (refresh 2: 4 states × 1 active). Only the bulk
       refresh body runs in PHASE_UPDATE; the just-re-pushed
       goal is skipped via `just_re_pushed_state`.
     - `cnt_phi_search=16` = 14 first-encounter + 2 goal
       re-pushes.
     - `cnt_phi_update=6` = 2 (refresh 1) + 4 (refresh 2);
       goal re-pushes accounted for in search.
     - `cnt_push=24` = 14 first-time + 2 goal re-pushes + 8
       bulk re-pushes (3 OPEN states after (3,0)-find + 5
       OPEN states after (3,3)-find).
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   37,
        'cnt_h_update':    8,
        'cnt_phi_search': 16,
        'cnt_phi_update':  6,
        'cnt_push':       24,
        'cnt_pop':        12,
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
     - `cnt_h_search=34` — first-encounter only; the vector
       cache absorbs every later h-read (goal re-push +
       refresh).
     - `cnt_h_update=0` — vector cache covers refresh too.
     - `cnt_phi_search=16` — same as nosv (Φ runs even when
       h is cached).
     - `cnt_phi_update=6` — same as nosv.
    ========================================================================
    """
    algo = _make_algo(is_lazy=False, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 16,
        'cnt_phi_update':  6,
        'cnt_push':       24,
        'cnt_pop':        12,
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
     - `cnt_h_search=37` — same as noopt (goal re-push h's
       are unconditional).
     - `cnt_h_update=5` = 2 (refresh 1, 1 state × 2 active)
       + 3 (refresh 2, 3 states × 1 active). Responsible-
       goal skip elides (1,1) in refresh-1 (resp=(3,3) still
       active) and (1,3) in refresh-2 (resp=(0,3) still
       active).
     - `cnt_phi_update=4` = 1 (refresh 1) + 3 (refresh 2).
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
     - `cnt_h_search=34` AND `cnt_h_update=0` (vector cached).
     - `cnt_phi_update=4` — responsible-goal opt skip + goal
       re-pushes accounted for in search.
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
     - `cnt_pop=18` = 12 real + 6 stale re-pops. The 6 stale
       pops break down as the 4 organic ones ((2,1) after
       (3,0)-find; (3,0)/(3,1)/(3,2) after (3,3)-find) PLUS
       2 from the lazy goal-repush skip ((3,0) right after
       (3,0)-find, (3,3) right after (3,3)-find — each
       goal's stale F is detected on its next pop and
       refreshed). The stale subset is derivable as
       cnt_pop − cnt_expanded − 3 on_goals = 18 − 9 − 3 = 6.
     - `cnt_push=22` = 14 first-time + 2 goal re-pushes + 6
       stale re-pushes (one per stale pop).
     - `cnt_h_search=69` = 34 first-encounter + 35 pop-time
       staleness (sum over the 18 _compute_F invocations in
       the lazy stale-pop branch of #active goals at call
       time). No `cnt_h_update` — lazy mode never enters
       PHASE_UPDATE.
     - `cnt_phi_search=32` = 14 first-encounter + 18 pop-
       time staleness.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   69,
        'cnt_h_update':    0,
        'cnt_phi_search': 32,
        'cnt_phi_update':  0,
        'cnt_push':       22,
        'cnt_pop':        18,
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
     - `cnt_h_search=34` — first-encounter only; the vector
       cache absorbs every later h-read (staleness check,
       deferred goal re-push staleness).
     - `cnt_phi_search=32` — same as nosv (Φ runs even when
       h is cached): 14 first-encounter + 18 stale-pop Φ-
       calls.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=False,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 32,
        'cnt_phi_update':  0,
        'cnt_push':       22,
        'cnt_pop':        18,
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
     - `cnt_phi_search=20` = 14 first-encounter + 6 stale-
       pop Φ-calls (the responsible-goal short-circuit skips
       pops whose responsible goal is still active).
     - `cnt_h_search=42` = 34 first-encounter + 8 stale-pop
       h-calls (sum over the 6 stale-pop `_compute_F`
       invocations of #active goals at call time).
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=False)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   42,
        'cnt_h_update':    0,
        'cnt_phi_search': 20,
        'cnt_phi_update':  0,
        'cnt_push':       22,
        'cnt_pop':        18,
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
     - `cnt_h_search=34` (vector cached) AND `cnt_h_update=0`.
     - `cnt_phi_search=20` — responsible-goal opt skip.
    ========================================================================
    """
    algo = _make_algo(is_lazy=True, is_opt=True,
                      store_vector=True)
    assert _run_and_strip_mem(algo) == {
        'cnt_h_search':   34,
        'cnt_h_update':    0,
        'cnt_phi_search': 20,
        'cnt_phi_update':  0,
        'cnt_push':       22,
        'cnt_pop':        18,
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
     design (and the lazy goal-repush skip) preserves this:
     under consistent h with MIN aggregation, a goal whose
     optimal path passes through another goal will see that
     other goal re-pop at f_new ≤ C* before it is found.
    ========================================================================
    """
    algo = _make_algo(is_lazy=is_lazy, is_opt=is_opt,
                      store_vector=store_vector)
    sol = algo.run()
    costs = {(g.key.row, g.key.col): s.cost
             for g, s in sol.per_goal.items()}
    assert costs == {(0, 3): 7, (3, 0): 3, (3, 3): 6}


@pytest.mark.parametrize('is_lazy', [False, True])
@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_lazy_update_counters_are_zero(
        is_lazy: bool,
        is_opt: bool,
        store_vector: bool) -> None:
    """
    ========================================================================
     Structural invariant (Path D): in lazy mode,
     `cnt_h_update == cnt_phi_update == 0`.

     Lazy mode never enters PHASE_UPDATE — its active-set-
     change response is folded into the search loop via pop-
     time staleness checks. This makes the counter axis
     mirror the structural `phase` axis exactly: both axes
     agree that lazy mode does "no work between sub-search
     segments".
    ========================================================================
    """
    algo = _make_algo(is_lazy=is_lazy, is_opt=is_opt,
                      store_vector=store_vector)
    algo.run()
    c = algo.counters
    if is_lazy:
        assert c['cnt_h_update'] == 0
        assert c['cnt_phi_update'] == 0
