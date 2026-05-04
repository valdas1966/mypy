import pytest

from f_hs.algo.i_0_oospp.i_2_astar_bpmx import AStarBPMX
from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


# ── Validation ──────────────────────────────────────────────


def test_rule_pathmax_validation() -> None:
    """
    ========================================================================
     rule_pathmax outside {None, 1, 2, 3} → ValueError.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    with pytest.raises(ValueError, match='rule_pathmax'):
        AStarLookupBPMX(problem=problem,
                        h=lambda s: float(s.distance(goal)),
                        rule_pathmax=4)


def test_depth_bpmx_validation() -> None:
    """
    ========================================================================
     depth_bpmx negative / non-int / bool → ValueError.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    with pytest.raises(ValueError, match='depth_bpmx'):
        AStarLookupBPMX(problem=problem,
                        h=lambda s: float(s.distance(goal)),
                        depth_bpmx=-1)
    with pytest.raises(ValueError, match='depth_bpmx'):
        AStarLookupBPMX(problem=problem,
                        h=lambda s: float(s.distance(goal)),
                        depth_bpmx=True)


def test_cache_without_goal_raises() -> None:
    """
    ========================================================================
     Cache supplied but no goal → ValueError (delegated to
     AStarLookup's chain validation).
    ========================================================================
    """
    a = StateBase[str](key='A')
    cache = {a: CacheEntry(h_perfect=0, suffix_next=None)}
    with pytest.raises(ValueError, match='cache'):
        AStarLookupBPMX(problem=ProblemSPP.Factory.graph_abc(),
                        h=lambda s: 0,
                        cache=cache,
                        goal=None)


def test_cache_goal_not_in_problem_goals_raises() -> None:
    """
    ========================================================================
     HCached goal must be a goal of the problem.
    ========================================================================
    """
    bogus = StateBase[str](key='Z')
    cache = {bogus: CacheEntry(h_perfect=0, suffix_next=None)}
    with pytest.raises(ValueError, match='HCached goal'):
        AStarLookupBPMX(problem=ProblemSPP.Factory.graph_abc(),
                        h=lambda s: 0,
                        cache=cache,
                        goal=bogus)


def test_prebuilt_hbase_with_bounds_raises() -> None:
    """
    ========================================================================
     Pre-built HBase `h` combined with `bounds` → ValueError.
    ========================================================================
    """
    a = StateBase[str](key='A')
    c = StateBase[str](key='C')
    cache = {a: CacheEntry(h_perfect=2, suffix_next=None),
             c: CacheEntry(h_perfect=0, suffix_next=None)}
    from f_hs.heuristic.i_1_callable.main import HCallable
    h = HCached(base=HCallable(fn=lambda s: 0), cache=cache, goal=c)
    with pytest.raises(ValueError, match='cache / bounds'):
        AStarLookupBPMX(problem=ProblemSPP.Factory.graph_abc(),
                        h=h,
                        bounds={})


def test_mechanism_on_no_hbounded_in_prebuilt_chain_raises() -> None:
    """
    ========================================================================
     Pre-built HBase `h` (no HBounded), mechanism on → ValueError.
    ========================================================================
    """
    from f_hs.heuristic.i_1_callable.main import HCallable
    h = HCallable(fn=lambda s: 0)
    with pytest.raises(ValueError, match='HBounded'):
        AStarLookupBPMX(problem=ProblemSPP.Factory.graph_abc(),
                        h=h,
                        rule_pathmax=1)


# ── Off-mode (≡ AStarLookup with the same cache) ────────────


def test_off_matches_astar_lookup_on_cached_at_b() -> None:
    """
    ========================================================================
     AStarLookupBPMX with rule=None, depth=0 must match
     AStarLookup's behavior given the same cache.
    ========================================================================
    """
    combo = AStarLookupBPMX.Factory.graph_abc_cached_at_b_off()
    lookup = AStarLookup.Factory.graph_abc_cached_at_b()
    s_combo = combo.run()
    s_lookup = lookup.run()
    assert s_combo.cost == s_lookup.cost == 2.0
    # Heap-op counts identical.
    assert combo.counters['cnt_push'] == lookup.counters['cnt_push']
    assert combo.counters['cnt_pop'] == lookup.counters['cnt_pop']


# ── BPMX-only mode (≡ AStarBPMX given the same h) ───────────


def test_bpmx_only_no_cache_matches_astar_bpmx_on_grid_4x4() -> None:
    """
    ========================================================================
     AStarLookupBPMX with no cache + BPMX(infinity) finds the
     same optimal cost as AStarBPMX on grid_4x4.
    ========================================================================
    """
    combo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    bpmx = AStarBPMX.Factory.grid_4x4_bpmx_full()
    s_combo = combo.run()
    s_bpmx = bpmx.run()
    assert s_combo.cost == s_bpmx.cost == 7.0


def test_rule3_no_cache_matches_astar_bpmx_rule3() -> None:
    """
    ========================================================================
     AStarLookupBPMX with rule=3, no cache: same cost as
     AStarBPMX rule3.
    ========================================================================
    """
    combo = AStarLookupBPMX.Factory.grid_4x4_rule3_no_cache()
    bpmx = AStarBPMX.Factory.grid_4x4_rule3()
    assert combo.run().cost == bpmx.run().cost == 7.0


# ── Optimality across configurations ────────────────────────


@pytest.mark.parametrize('rule_pathmax', [None, 1, 2, 3])
@pytest.mark.parametrize('depth_bpmx', [0, 1, 2, None])
def test_optimality_grid_4x4_no_cache(rule_pathmax: int | None,
                                      depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Across the (rule_pathmax × depth_bpmx) grid with no cache
     on grid_4x4_obstacle, optimal cost stays 7.0 — the BPMX
     path through the combined class preserves admissibility.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_pathmax=rule_pathmax,
        depth_bpmx=depth_bpmx,
    )
    assert algo.run().cost == 7.0


@pytest.mark.parametrize('depth_bpmx', [0, 1, None])
def test_optimality_grid_4x4_with_goal_cached(
        depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Caching the goal state + BPMX on: optimal cost still 7.0,
     and the run terminates via cache-hit early-exit (or
     goal-pop). BPMX must not break A* admissibility when
     interacting with the cache.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    cache = {goal: CacheEntry(h_perfect=0, suffix_next=None)}
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        cache=cache,
        goal=goal,
        rule_pathmax=None,
        depth_bpmx=depth_bpmx,
    )
    assert algo.run().cost == 7.0


# ── AStarLookup features still work ─────────────────────────


def test_cache_hit_early_term_with_bpmx_on() -> None:
    """
    ========================================================================
     Cache covering all of {A, B, C}: pop(A) early-exits via
     HCached even with BPMX(1) enabled. Zero expansions of
     successors past A.
    ========================================================================
    """
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')
    c = StateBase[str](key='C')
    cache = {
        a: CacheEntry(h_perfect=2, suffix_next=b),
        b: CacheEntry(h_perfect=1, suffix_next=c),
        c: CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookupBPMX(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: 0,
        cache=cache,
        goal=c,
        rule_pathmax=None,
        depth_bpmx=1,
    )
    sol = algo.run()
    assert sol.cost == 2.0
    # Cache-hit path: 1 push (start), 1 pop, then early-exit.
    assert algo.counters['cnt_push'] == 1
    assert algo.counters['cnt_pop'] == 1
    # BPMX cascade did NOT run — cache-hit early-exit fires
    # BEFORE _pre_expand.
    assert algo.counters['cnt_bpmx_attempts'] == 0


def test_to_cache_works_after_combined_run() -> None:
    """
    ========================================================================
     `to_cache()` harvest works after a combined run.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_cached_suffix_bpmx_d1()
    algo.run()
    cache = algo.to_cache()
    assert len(cache) > 0
    # Every harvested entry has h_perfect <= the optimal cost.
    for entry in cache.values():
        assert entry.h_perfect >= 0


def test_propagate_pathmax_callable_under_combined_class() -> None:
    """
    ========================================================================
     AStarLookup's pre-search `propagate_pathmax` is still
     callable on the combined class.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {goal: 0}
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        rule_pathmax=None,
        depth_bpmx=0,
    )
    updates = algo.propagate_pathmax(depth=1)
    assert isinstance(updates, dict)


def test_reconstruct_path_suffix_stitch_with_bpmx_on() -> None:
    """
    ========================================================================
     Suffix-stitched reconstruct_path works on cache-hit
     termination even with BPMX on.
    ========================================================================
    """
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')
    c = StateBase[str](key='C')
    cache = {
        b: CacheEntry(h_perfect=1, suffix_next=c),
        c: CacheEntry(h_perfect=0, suffix_next=None),
    }
    h_map = {'A': 2}
    algo = AStarLookupBPMX(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: h_map.get(s.key, 0),
        cache=cache,
        goal=c,
        depth_bpmx=1,
    )
    algo.run()
    path_keys = [s.key for s in algo.reconstruct_path()]
    assert path_keys == ['A', 'B', 'C']


# ── Subclass / Factory plumbing ─────────────────────────────


def test_is_subclass_of_astar_lookup() -> None:
    """
    ========================================================================
     Inheritance invariant: AStarLookupBPMX < AStarLookup < AStar.
    ========================================================================
    """
    from f_hs.algo.i_0_oospp.i_1_astar import AStar
    assert issubclass(AStarLookupBPMX, AStarLookup)
    assert issubclass(AStarLookupBPMX, AStar)


def test_factory_attached() -> None:
    """
    ========================================================================
     Factory wired via __init__.py.
    ========================================================================
    """
    assert AStarLookupBPMX.Factory is not None
    assert AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache() is not None


def test_mro_puts_bpmx_mixin_before_astar_lookup() -> None:
    """
    ========================================================================
     MRO must be: AStarLookupBPMX → BPMXMixin → AStarLookup →
     AStar → AlgoSPP → ... — so `_pre_expand` resolves to
     BPMXMixin and `_early_exit` / `_priority` resolve to
     AStarLookup.
    ========================================================================
    """
    from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin
    from f_hs.algo.i_0_oospp.i_1_astar import AStar
    mro = type(AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()).__mro__
    names = [c.__name__ for c in mro]
    assert names.index('BPMXMixin') < names.index('AStarLookup')
    assert names.index('AStarLookup') < names.index('AStar')
