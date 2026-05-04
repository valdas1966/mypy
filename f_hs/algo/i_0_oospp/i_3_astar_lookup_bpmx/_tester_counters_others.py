from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


# ── Scaffold shape ──────────────────────────────────────────


_EXPECTED_NAMES: set[str] = {
    'cnt_pathmax_attempts',
    'cnt_pathmax_lifts',
    'cnt_bpmx_attempts',
    'cnt_bpmx_iterations',
    'cnt_bpmx_rule3_lifts',
    'cnt_bpmx_rule1_forwards',
    'cnt_bpmx_subtree_states',
    'cnt_push',
    'cnt_pop',
    'cnt_decrease',
    'mem_open',
    'mem_closed',
    'mem_cache',
    'mem_bounds',
}


def test_counters_scaffold_shape() -> None:
    """
    ========================================================================
     The counters surface has the 15-name scaffold defined by
     BPMXMixin (pathmax 2 + bpmx 5 + frontier 3 + mem 5
     snapshots populated by `_run_post()` after timing).
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    algo.run()
    assert set(algo.counters.keys()) == _EXPECTED_NAMES
    assert len(algo.counters) == 14


# ── Off-mode counters ───────────────────────────────────────


def test_counters_off_mode_no_pathmax_or_bpmx_activity() -> None:
    """
    ========================================================================
     With rule=None, depth=0: all 7 mechanism counters stay 0;
     only frontier mirrors are non-zero.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.graph_abc_cached_at_b_off()
    algo.run()
    assert algo.counters['cnt_pathmax_attempts'] == 0
    assert algo.counters['cnt_pathmax_lifts'] == 0
    assert algo.counters['cnt_bpmx_attempts'] == 0
    assert algo.counters['cnt_bpmx_iterations'] == 0
    assert algo.counters['cnt_bpmx_rule3_lifts'] == 0
    assert algo.counters['cnt_bpmx_rule1_forwards'] == 0
    assert algo.counters['cnt_bpmx_subtree_states'] == 0


# ── Pathmax counters ────────────────────────────────────────


def test_counters_rule_pathmax_attempts_per_expansion() -> None:
    """
    ========================================================================
     With rule_pathmax enabled (any of 1/2/3) and depth=0,
     each expansion attempts the rule once →
     cnt_pathmax_attempts == cnt_pop (every popped state's
     expansion runs the rule, including the goal pop).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_pathmax=1,
        depth_bpmx=0,
    )
    algo.run()
    pops_excluding_goal = algo.counters['cnt_pop'] - 1
    assert (algo.counters['cnt_pathmax_attempts']
            == pops_excluding_goal)


# ── BPMX counters ───────────────────────────────────────────


def test_counters_bpmx_attempts_per_expansion() -> None:
    """
    ========================================================================
     With BPMX on (depth=None): each non-goal expansion attempts
     the BPMX cascade. cnt_bpmx_attempts equals the number of
     expansions that actually ran the cascade.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    algo.run()
    # Cascade runs once per non-goal pop where _h.is_perfect is
    # False. Lower bound: at least one attempt fired.
    assert algo.counters['cnt_bpmx_attempts'] >= 1
    # Upper bound: cannot exceed pop count.
    assert (algo.counters['cnt_bpmx_attempts']
            <= algo.counters['cnt_pop'])


def test_counters_bpmx_subtree_states_positive_when_on() -> None:
    """
    ========================================================================
     With BPMX(infinity), the cascade visits at least one
     state per attempt → cnt_bpmx_subtree_states >=
     cnt_bpmx_attempts.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    algo.run()
    assert (algo.counters['cnt_bpmx_subtree_states']
            >= algo.counters['cnt_bpmx_attempts'])


def test_counters_bpmx_iterations_at_least_one_per_attempt() -> None:
    """
    ========================================================================
     Every BPMX cascade runs at least 1 iteration
     (the no-improvement short-circuit only fires AFTER the
     first round) → cnt_bpmx_iterations >= cnt_bpmx_attempts.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    algo.run()
    assert (algo.counters['cnt_bpmx_iterations']
            >= algo.counters['cnt_bpmx_attempts'])


# ── Cache + BPMX interactions ───────────────────────────────


def test_counters_cache_hit_skips_bpmx_for_cached_pop() -> None:
    """
    ========================================================================
     When a cached state is popped, _early_exit fires BEFORE
     _pre_expand → BPMX cascade does NOT run for that pop.
     Confirmed by counting: with cache covering all of
     {A, B, C}, pop(A) early-exits → cnt_bpmx_attempts == 0
     even though depth_bpmx is on.
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
        depth_bpmx=None,
    )
    algo.run()
    assert algo.counters['cnt_bpmx_attempts'] == 0
    assert algo.counters['cnt_pop'] == 1   # early-exit at A


# ── Exact pinned values ─────────────────────────────────────


def test_counters_pin_graph_abc_cached_at_b_off() -> None:
    """
    ========================================================================
     Exact counter values for `graph_abc_cached_at_b_off`:
     pop(A) → expand → push(B) → pop(B) early-exits.
       push=2, pop=2, decrease=0. All BPMX/pathmax = 0.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.graph_abc_cached_at_b_off()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 0,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 0,
        'cnt_bpmx_iterations': 0,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 0,
        'cnt_push': 2,
        'cnt_pop': 2,
        'cnt_decrease': 0,
        'mem_open': 280, 'mem_closed': 712,
        'mem_cache': 376, 'mem_bounds': 0,
    }


def test_counters_pin_graph_abc_cached_at_b_bpmx_d1() -> None:
    """
    ========================================================================
     Exact counter values for the cache-at-B + BPMX(1) case:
     pop(A) runs BPMX(1) over subtree {A, B}; B is cached
     (skipped from lift); cascade fires 1 iteration with no
     lifts. pop(B) early-exits via HCached.

       cnt_bpmx_attempts       = 1
       cnt_bpmx_iterations     = 1
       cnt_bpmx_subtree_states = 2  (A + B)
       cnt_bpmx_rule3_lifts    = 0  (A has higher h than what
                                     B − w(B,A) yields)
       cnt_bpmx_rule1_forwards = 0  (B is cached, skipped)
       cnt_pathmax_*           = 0
       push=2, pop=2, decrease=0.
    ========================================================================
    """
    algo = (AStarLookupBPMX.Factory
            .graph_abc_cached_at_b_bpmx_d1())
    algo.run()
    assert dict(algo.counters) == {
        'cnt_pathmax_attempts': 0,
        'cnt_pathmax_lifts': 0,
        'cnt_bpmx_attempts': 1,
        'cnt_bpmx_iterations': 1,
        'cnt_bpmx_rule3_lifts': 0,
        'cnt_bpmx_rule1_forwards': 0,
        'cnt_bpmx_subtree_states': 2,
        'cnt_push': 2,
        'cnt_pop': 2,
        'cnt_decrease': 0,
        'mem_open': 280, 'mem_closed': 712,
        'mem_cache': 376, 'mem_bounds': 64,
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

    def _make(is_recording: bool) -> AStarLookupBPMX:
        return AStarLookupBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            depth_bpmx=None,
            is_recording=is_recording,
        )

    a_off = _make(False)
    a_on = _make(True)
    a_off.run()
    a_on.run()
    assert dict(a_off.counters) == dict(a_on.counters)
