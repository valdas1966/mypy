from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


# ── Scaffold shape ──────────────────────────────────────────


_EXPECTED_NAMES: set[str] = {
    'cnt_prop_waves',
    'cnt_prop_attempts',
    'cnt_prop_lifts',
    'cnt_bpmx_attempts',
    'cnt_bpmx_successes',
    'cnt_bpmx_depth',
    'cnt_push',
    'cnt_pop',
    'cnt_decrease',
    'cnt_expanded',
    'cnt_generated',
    'mem_open',
    'mem_closed',
    'mem_cache',
    'mem_bounds',
}


def test_counters_scaffold_shape() -> None:
    """
    ========================================================================
     The counters surface has the 15-name scaffold (propagate
     3 + bpmx 3 + frontier 3 + search-semantic 2 + memory 4)
     declared by AStarLookup's `_COUNTER_NAMES` override.
    ========================================================================
    """
    algo = AStarLookup.Factory.grid_4x4(
        rule_bpmx='CASCADE', depth_bpmx=None)
    algo.run()
    assert set(algo.counters.keys()) == _EXPECTED_NAMES
    assert len(algo.counters) == 15


# ── Off-mode counters ───────────────────────────────────────


def test_counters_off_mode_no_bpmx_activity() -> None:
    """
    ========================================================================
     With rule_bpmx=None: all 3 BPMX-mechanism counters stay 0;
     only frontier mirrors are non-zero.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo.run()
    assert algo.counters['cnt_bpmx_attempts'] == 0
    assert algo.counters['cnt_bpmx_successes'] == 0
    assert algo.counters['cnt_bpmx_depth'] == 0


# ── Pathmax counters ────────────────────────────────────────


def test_counters_attempts_per_expansion() -> None:
    """
    ========================================================================
     With any rule_bpmx active and depth=1 on a no-cache run,
     each non-goal expansion increments cnt_bpmx_attempts once.
     cnt_bpmx_attempts == cnt_pop − 1.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx='1',
        depth_bpmx=1,
    )
    algo.run()
    assert (algo.counters['cnt_bpmx_attempts']
            == algo.counters['cnt_pop'] - 1)


# ── BPMX cascade counters ───────────────────────────────────


def test_counters_cascade_attempts_per_expansion() -> None:
    """
    ========================================================================
     With CASCADE on (depth=None): each non-goal expansion
     attempts the cascade. cnt_bpmx_attempts equals the number
     of expansions that actually ran the cascade, bounded by
     cnt_pop.
    ========================================================================
    """
    algo = AStarLookup.Factory.grid_4x4(
        rule_bpmx='CASCADE', depth_bpmx=None)
    algo.run()
    assert algo.counters['cnt_bpmx_attempts'] >= 1
    assert (algo.counters['cnt_bpmx_attempts']
            <= algo.counters['cnt_pop'])


# ── Cache + BPMX interactions ───────────────────────────────


def test_counters_cache_hit_skips_bpmx_for_cached_pop() -> None:
    """
    ========================================================================
     When a cached state is popped, _early_exit fires BEFORE
     _pre_expand → the cascade does NOT run for that pop.
     Confirmed by counting: with cache covering all of
     {A, B, C}, pop(A) early-exits → cnt_bpmx_attempts == 0
     even though CASCADE is on.
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
    algo = AStarLookup(
        problem=ProblemSPP.Factory.graph_abc(),
        h=lambda s: 0,
        cache=cache,
        goal=c,
        rule_bpmx='CASCADE',
        depth_bpmx=None,
    )
    algo.run()
    assert algo.counters['cnt_bpmx_attempts'] == 0
    assert algo.counters['cnt_pop'] == 1   # early-exit at A


# ── Exact pinned values ─────────────────────────────────────


def test_counters_pin_graph_abc_cached_at_b_off() -> None:
    """
    ========================================================================
     Exact counter values for `graph_abc_cached_at_b()`
     in off-mode (rule_bpmx=None):
     pop(A) → expand → push(B) → pop(B) early-exits.
       push=2, pop=2, decrease=0. All BPMX counters = 0.
    ========================================================================
    """
    algo = AStarLookup.Factory.graph_abc_cached_at_b()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 2,
        'cnt_pop': 2,
        'cnt_decrease': 0,
        'cnt_expanded': 1,
        'cnt_generated': 2,
    }


def test_counters_pin_graph_abc_cached_at_b_cascade_d1() -> None:
    """
    ========================================================================
     Exact counter values for the cache-at-B + CASCADE depth=1
     case: pop(A) runs the cascade over subtree {A, B}; B is
     cached (skipped from lift); cascade settles with no lifts.
     pop(B) early-exits via HCached.

       cnt_bpmx_attempts   = 1
       cnt_bpmx_successes  = 0  (A has higher h than
         B − w(B,A); B is cached and skipped from forwards)
       cnt_bpmx_depth      = 0  (no lifts ever fired)
       push=2, pop=2, decrease=0.
    ========================================================================
    """
    algo = (AStarLookup.Factory
            .graph_abc_cached_at_b(rule_bpmx='CASCADE',
                                   depth_bpmx=1,
                                   is_recording=True))
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_prop_waves': 0,
        'cnt_prop_attempts': 0,
        'cnt_prop_lifts': 0,
        'cnt_bpmx_attempts': 1,
        'cnt_bpmx_successes': 0,
        'cnt_bpmx_depth': 0,
        'cnt_push': 2,
        'cnt_pop': 2,
        'cnt_decrease': 0,
        'cnt_expanded': 1,
        'cnt_generated': 2,
    }


# ── Recording independence ──────────────────────────────────


def test_counters_independent_of_recording_flag() -> None:
    """
    ========================================================================
     Counter values do not depend on whether is_recording is
     True. Two runs of the same factory configuration with
     opposite recording settings yield the same counter dict.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal

    def _make(is_recording: bool) -> AStarLookup:
        return AStarLookup(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_bpmx='CASCADE',
            depth_bpmx=None,
            is_recording=is_recording,
        )

    a_off = _make(False)
    a_on = _make(True)
    a_off.run()
    a_on.run()
    assert dict(a_off.counters) == dict(a_on.counters)
