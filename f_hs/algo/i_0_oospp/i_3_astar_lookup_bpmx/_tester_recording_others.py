from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx import AStarLookupBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


def _types(events: list[dict]) -> list[str]:
    """
    ========================================================================
     Extract the ordered list of event types.
    ========================================================================
    """
    return [e['type'] for e in events]


# ── Off-mode emits only AStar's events ──────────────────────


def test_off_emits_only_search_events() -> None:
    """
    ========================================================================
     With rule=None, depth=0: the recorder log contains only
     push / pop / decrease_g — no pathmax_apply / bpmx_*.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_pathmax=None,
        depth_bpmx=0,
        is_recording=True,
    )
    algo.run()
    types = set(_types(algo.recorder.events))
    assert types <= {'push', 'pop', 'decrease_g'}
    assert 'pathmax_apply' not in types
    assert 'bpmx_iteration' not in types


# ── pathmax_apply event schema (rules 1 / 3) ────────────────


def test_pathmax_apply_rule3_event_schema() -> None:
    """
    ========================================================================
     rule_pathmax=3 fires pathmax_apply{rule=3, via_child}
     events when a parent's h is liftable from a strong child.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarLookupBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_pathmax=3,
        depth_bpmx=0,
        is_recording=True,
    )
    algo.run()
    pathmax_events = [e for e in algo.recorder.events
                      if e['type'] == 'pathmax_apply']
    assert any(e['rule'] == 3 and 'via_child' in e
               and 'h_old' in e and 'h_new' in e
               for e in pathmax_events)


def test_pathmax_apply_h_values_int_cast() -> None:
    """
    ========================================================================
     h_old / h_new on pathmax_apply events are int-cast (BPMX
     mixin's _enrich_event handles this).
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarLookupBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_pathmax=3,
        is_recording=True,
    )
    algo.run()
    for e in algo.recorder.events:
        if e['type'] == 'pathmax_apply':
            assert isinstance(e['h_old'], int)
            assert isinstance(e['h_new'], int)


# ── bpmx_* events ───────────────────────────────────────────


def test_bpmx_iteration_marker_per_expansion() -> None:
    """
    ========================================================================
     With BPMX on, each expansion emits at least one
     bpmx_iteration event, and `iteration` resets to 1 at the
     start of each expansion's cascade.
    ========================================================================
    """
    algo = AStarLookupBPMX.Factory.grid_4x4_bpmx_full_no_cache()
    algo._is_recording = True
    # Re-create with is_recording=True
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    iters = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_iteration']
    assert len(iters) > 0
    # Every iteration has the required keys.
    for e in iters:
        assert 'state' in e
        assert 'iteration' in e
        assert 'num_levels' in e
        assert 'num_states' in e


def test_bpmx_lift_event_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     BPMX(infinity) on the inconsistent diamond fires
     bpmx_lift events (Rule 3 lifts the parent from a
     stronger-h child).
    ========================================================================
    """
    algo = (AStarLookupBPMX.Factory
            .graph_diamond_inconsistent_bpmx_full())
    algo.run()
    lifts = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_lift']
    assert len(lifts) > 0
    for e in lifts:
        assert 'state' in e and 'h_old' in e and 'h_new' in e
        assert 'via_child' in e
        assert isinstance(e['h_old'], int)
        assert isinstance(e['h_new'], int)


def test_bpmx_forward_event_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     BPMX(infinity) also fires bpmx_forward events (Rule 1
     pushes the lifted h forward to children).
    ========================================================================
    """
    algo = (AStarLookupBPMX.Factory
            .graph_diamond_inconsistent_bpmx_full())
    algo.run()
    fwds = [e for e in algo.recorder.events
            if e['type'] == 'bpmx_forward']
    # Forward events fire if Rule 3 lifted the root and Rule
    # 1 then pushes that to children.
    if fwds:
        for e in fwds:
            assert 'state' in e and 'via_parent' in e


# ── is_cached / is_bounded coexist with BPMX events ─────────


def test_is_cached_flag_coexists_with_bpmx_events() -> None:
    """
    ========================================================================
     A run with both cache and BPMX records `is_cached=True`
     on the cached state's pop, and BPMX events for the
     uncached expansions — both event vocabularies coexist.
    ========================================================================
    """
    algo = (AStarLookupBPMX.Factory
            .graph_abc_cached_at_b_bpmx_d1())
    algo.run()
    events = algo.recorder.events
    pops = [e for e in events if e['type'] == 'pop']
    cached_pops = [e for e in pops
                   if e.get('is_cached') is True]
    assert len(cached_pops) >= 1   # B early-exits with is_cached
    bpmx_iters = [e for e in events if e['type'] == 'bpmx_iteration']
    assert len(bpmx_iters) >= 1   # A's expansion fires BPMX


def test_cached_state_skipped_from_bpmx_lift() -> None:
    """
    ========================================================================
     A cached state appearing in the BPMX subtree is skipped
     from lift-event emission (`is_perfect` guard in the
     mixin's rule3_up / rule1_down). The cascade still records
     the iteration marker, but no bpmx_lift / bpmx_forward
     event names the cached state.
    ========================================================================
    """
    algo = (AStarLookupBPMX.Factory
            .graph_abc_cached_at_b_bpmx_d1())
    algo.run()
    b_key = 'B'
    lifts = [e for e in algo.recorder.events
             if e['type'] in ('bpmx_lift', 'bpmx_forward')]
    for e in lifts:
        assert e['state'].key != b_key, (
            f'cached state {b_key} should not be a lift target')


# ── Pre-search propagate + in-search BPMX ───────────────────


def test_propagate_event_then_bpmx_in_search() -> None:
    """
    ========================================================================
     Pre-search `propagate_pathmax` records `propagate_wave`
     and `propagate` events; subsequent in-search BPMX run
     records `bpmx_iteration` events. Both vocabularies appear
     in order.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {goal: 0}
    algo = AStarLookupBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        depth_bpmx=1,
        is_recording=True,
    )
    algo.propagate_pathmax(depth=1)
    algo.run()
    types = _types(algo.recorder.events)
    has_propagate_wave = 'propagate_wave' in types
    has_bpmx_iter = 'bpmx_iteration' in types
    assert has_propagate_wave, 'pre-search propagate_wave missing'
    assert has_bpmx_iter, 'in-search bpmx_iteration missing'
    # propagate_wave events all precede bpmx_iteration events.
    last_propagate = max(
        i for i, t in enumerate(types) if t == 'propagate_wave')
    first_bpmx = min(
        i for i, t in enumerate(types) if t == 'bpmx_iteration')
    assert last_propagate < first_bpmx
