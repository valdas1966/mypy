import pytest

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


# ── Validation ──────────────────────────────────────────────


def test_rule_bpmx_validation() -> None:
    """
    ========================================================================
     rule_bpmx outside {None, '1', '2', '3', 'CASCADE'} →
     ValueError.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    with pytest.raises(ValueError, match='rule_bpmx'):
        AStarBPMX(problem=problem,
                        h=lambda s: float(s.distance(goal)),
                        rule_bpmx='4')


def test_depth_bpmx_validation() -> None:
    """
    ========================================================================
     depth_bpmx 0 / negative / non-int / bool → ValueError.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    for bad in (0, -1, True):
        with pytest.raises(ValueError, match='depth_bpmx'):
            AStarBPMX(problem=problem,
                            h=lambda s: float(s.distance(goal)),
                            rule_bpmx='1',
                            depth_bpmx=bad)


def test_rule2_requires_depth_1() -> None:
    """
    ========================================================================
     Rule 2 cannot propagate beyond depth 1 — depth_bpmx > 1
     and None are both rejected.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    for bad in (2, 5, None):
        with pytest.raises(ValueError, match='Rule 2'):
            AStarBPMX(problem=problem,
                            h=lambda s: float(s.distance(goal)),
                            rule_bpmx='2',
                            depth_bpmx=bad)


def test_cache_without_goal_raises() -> None:
    """
    ========================================================================
     Cache supplied but no goal → ValueError (delegated to
     AStarBPMX's chain validation).
    ========================================================================
    """
    a = StateBase[str](key='A')
    cache = {a: CacheEntry(h_perfect=0, suffix_next=None)}
    with pytest.raises(ValueError, match='cache'):
        AStarBPMX(problem=ProblemSPP.Factory.graph_abc(),
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
        AStarBPMX(problem=ProblemSPP.Factory.graph_abc(),
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
        AStarBPMX(problem=ProblemSPP.Factory.graph_abc(),
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
        AStarBPMX(problem=ProblemSPP.Factory.graph_abc(),
                        h=h,
                        rule_bpmx='1')


# ── Off-mode (≡ AStarBPMX with the same cache) ────────────


def test_off_matches_astar_lookup_on_cached_at_b() -> None:
    """
    ========================================================================
     AStarBPMX with rule_bpmx=None must match
     AStarBPMX's behavior given the same cache.
    ========================================================================
    """
    combo = AStarBPMX.Factory.graph_abc_cached_at_b()
    lookup = AStarBPMX.Factory.graph_abc_cached_at_b()
    s_combo = combo.run()
    s_lookup = lookup.run()
    assert s_combo.cost == s_lookup.cost == 2.0
    assert combo.counters['cnt_push'] == lookup.counters['cnt_push']
    assert combo.counters['cnt_pop'] == lookup.counters['cnt_pop']


# ── Optimality across configurations ────────────────────────


@pytest.mark.parametrize('rule_bpmx,depth_bpmx', [
    (None, 1),
    ('1', 1), ('1', 2), ('1', None),
    ('2', 1),
    ('3', 1), ('3', 2), ('3', None),
    ('CASCADE', 1), ('CASCADE', 2), ('CASCADE', None),
])
def test_optimality_grid_4x4_no_cache(rule_bpmx: str | None,
                                      depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Across the (rule_bpmx × depth_bpmx) valid grid with no
     cache on grid_4x4_obstacle, optimal cost stays 7.0.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx=rule_bpmx,
        depth_bpmx=depth_bpmx,
    )
    assert algo.run().cost == 7.0


@pytest.mark.parametrize('rule_bpmx,depth_bpmx', [
    (None, 1),
    ('CASCADE', 1), ('CASCADE', None),
    ('1', 1), ('3', 1),
])
def test_optimality_grid_4x4_with_goal_cached(
        rule_bpmx: str | None,
        depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Caching the goal state + BPMX on: optimal cost still 7.0,
     and the run terminates via cache-hit early-exit (or
     goal-pop).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    cache = {goal: CacheEntry(h_perfect=0, suffix_next=None)}
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        cache=cache,
        goal=goal,
        rule_bpmx=rule_bpmx,
        depth_bpmx=depth_bpmx,
    )
    assert algo.run().cost == 7.0


# ── AStarBPMX features still work ─────────────────────────


def test_cache_hit_early_term_with_bpmx_on() -> None:
    """
    ========================================================================
     Cache covering all of {A, B, C}: pop(A) early-exits via
     HCached even with CASCADE enabled. Zero expansions of
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
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: 0,
        cache=cache,
        goal=c,
        rule_bpmx='CASCADE',
        depth_bpmx=1,
    )
    sol = algo.run()
    assert sol.cost == 2.0
    assert algo.counters['cnt_push'] == 1
    assert algo.counters['cnt_pop'] == 1
    # Cascade did NOT run — cache-hit early-exit fires
    # BEFORE _pre_expand.
    assert algo.counters['cnt_bpmx_attempts'] == 0


def test_to_cache_works_after_combined_run() -> None:
    """
    ========================================================================
     `to_cache()` harvest works after a combined run.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_cached_suffix_cascade_d1()
    algo.run()
    cache = algo.to_cache()
    assert len(cache) > 0
    for entry in cache.values():
        assert entry.h_perfect >= 0


def test_propagate_pathmax_callable_under_combined_class() -> None:
    """
    ========================================================================
     AStarBPMX's pre-search `propagate_pathmax` is still
     callable on the combined class.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {goal: 0}
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        rule_bpmx=None,
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
    b = StateBase[str](key='B')
    c = StateBase[str](key='C')
    cache = {
        b: CacheEntry(h_perfect=1, suffix_next=c),
        c: CacheEntry(h_perfect=0, suffix_next=None),
    }
    h_map = {'A': 2}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: h_map.get(s.key, 0),
        cache=cache,
        goal=c,
        rule_bpmx='CASCADE',
        depth_bpmx=1,
    )
    algo.run()
    path_keys = [s.key for s in algo.reconstruct_path()]
    assert path_keys == ['A', 'B', 'C']


# ── Subclass / Factory plumbing ─────────────────────────────


def test_is_subclass_of_astar_lookup() -> None:
    """
    ========================================================================
     Inheritance invariant: AStarBPMX < AStarBPMX < AStar.
    ========================================================================
    """
    from f_hs.algo.i_0_oospp.i_1_astar import AStar
    assert issubclass(AStarBPMX, AStarBPMX)
    assert issubclass(AStarBPMX, AStar)


def test_factory_attached() -> None:
    """
    ========================================================================
     Factory wired via __init__.py.
    ========================================================================
    """
    assert AStarBPMX.Factory is not None
    assert AStarBPMX.Factory.grid_4x4(
        rule_bpmx='CASCADE', depth_bpmx=None) is not None


def test_mro_puts_bpmx_mixin_before_astar() -> None:
    """
    ========================================================================
     Post-Phase-1 MRO: AStarBPMX → AStarBPMX →
     BPMXMixin → AStar → AlgoSPP → ... — `AStarBPMX` now
     natively composes BPMXMixin, so the mixin sits between
     `AStarBPMX` and `AStar` (mechanism overrides resolve
     before the simple-A* fallback).
    ========================================================================
    """
    mro = type(AStarBPMX.Factory.grid_4x4(
        rule_bpmx='CASCADE', depth_bpmx=None)).__mro__
    names = [c.__name__ for c in mro]
    assert names.index('AStarBPMX') < names.index('BPMXMixin')
    assert names.index('BPMXMixin') < names.index('AStar')
