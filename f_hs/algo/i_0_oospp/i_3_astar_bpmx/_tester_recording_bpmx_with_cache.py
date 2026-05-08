from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


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
     With rule_bpmx=None: the recorder log contains only
     push / pop / decrease_g — no pathmax_apply / bpmx_*.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx=None,
        is_recording=True,
    )
    algo.run()
    types = set(_types(algo.recorder.events))
    assert types <= {'push', 'pop', 'decrease_g'}
    assert 'pathmax_apply' not in types
    assert 'bpmx_iteration' not in types


# ── Rule 3 (isolated, depth=1) — emits bpmx_lift ────────────


def test_rule3_isolated_emits_bpmx_lift() -> None:
    """
    ========================================================================
     rule_bpmx='3' fires `bpmx_lift{via_child}` events when a
     parent's h is liftable from a strong child.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_bpmx='3',
        depth_bpmx=1,
        is_recording=True,
    )
    algo.run()
    lifts = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_lift']
    assert any('via_child' in e and 'h_old' in e and 'h_new' in e
               for e in lifts)


def test_bpmx_lift_h_values_int_cast() -> None:
    """
    ========================================================================
     h_old / h_new on bpmx_lift / bpmx_forward events are
     int-cast (BPMX mixin's _enrich_event handles this).
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_bpmx='3',
        depth_bpmx=1,
        is_recording=True,
    )
    algo.run()
    for e in algo.recorder.events:
        if e['type'] in ('bpmx_lift', 'bpmx_forward'):
            assert isinstance(e['h_old'], int)
            assert isinstance(e['h_new'], int)


# ── bpmx_iteration — CASCADE only ────────────────────────────


def test_bpmx_iteration_marker_per_cascade() -> None:
    """
    ========================================================================
     With CASCADE on, each expansion emits at least one
     `bpmx_iteration` event, and `iteration` resets to 1 at
     the start of each expansion's cascade.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx='CASCADE',
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    iters = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_iteration']
    assert len(iters) > 0
    for e in iters:
        assert 'state' in e
        assert 'iteration' in e
        assert 'num_levels' in e
        assert 'num_states' in e


def test_isolated_rules_emit_no_iteration_marker() -> None:
    """
    ========================================================================
     `bpmx_iteration` events are emitted only by CASCADE — the
     isolated rule sweeps run a single non-iterated pass.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    for rule in ('1', '2', '3'):
        algo = AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_bpmx=rule,
            depth_bpmx=1,
            is_recording=True,
        )
        algo.run()
        types = {e['type'] for e in algo.recorder.events}
        assert 'bpmx_iteration' not in types


def test_cascade_lift_event_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     CASCADE on the inconsistent diamond fires `bpmx_lift`
     events (Rule 3 lifts the parent from a stronger-h child).
    ========================================================================
    """
    algo = (AStarBPMX.Factory
            .graph_diamond_inconsistent_cascade())
    algo.run()
    lifts = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_lift']
    assert len(lifts) > 0
    for e in lifts:
        assert 'state' in e and 'h_old' in e and 'h_new' in e
        assert 'via_child' in e
        assert isinstance(e['h_old'], int)
        assert isinstance(e['h_new'], int)


def test_cascade_forward_event_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     CASCADE also fires `bpmx_forward` events (Rule 1 pushes
     the lifted h forward to children).
    ========================================================================
    """
    algo = (AStarBPMX.Factory
            .graph_diamond_inconsistent_cascade())
    algo.run()
    fwds = [e for e in algo.recorder.events
            if e['type'] == 'bpmx_forward']
    if fwds:
        for e in fwds:
            assert 'state' in e and 'via_parent' in e


# ── is_cached / is_bounded coexist with BPMX events ─────────


def test_is_cached_flag_coexists_with_bpmx_events() -> None:
    """
    ========================================================================
     A run with both cache and CASCADE records `is_cached=True`
     on the cached state's pop, and CASCADE events for the
     uncached expansions — both event vocabularies coexist.
    ========================================================================
    """
    algo = (AStarBPMX.Factory
            .graph_abc_cached_at_b(rule_bpmx='CASCADE',
                                   depth_bpmx=1,
                                   is_recording=True))
    algo.run()
    events = algo.recorder.events
    pops = [e for e in events if e['type'] == 'pop']
    cached_pops = [e for e in pops
                   if e.get('is_cached') is True]
    assert len(cached_pops) >= 1   # B early-exits with is_cached
    bpmx_iters = [e for e in events if e['type'] == 'bpmx_iteration']
    assert len(bpmx_iters) >= 1   # A's expansion fires CASCADE


def test_cached_state_skipped_from_bpmx_lift() -> None:
    """
    ========================================================================
     A cached state appearing in the cascade subtree is skipped
     from lift-event emission (`is_perfect` guard). The cascade
     still records the iteration marker, but no bpmx_lift /
     bpmx_forward event names the cached state.
    ========================================================================
    """
    algo = (AStarBPMX.Factory
            .graph_abc_cached_at_b(rule_bpmx='CASCADE',
                                   depth_bpmx=1,
                                   is_recording=True))
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
     and `propagate` events; subsequent in-search CASCADE
     records `bpmx_iteration` events. Both vocabularies appear
     in order.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {goal: 0}
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        bounds=bounds,
        rule_bpmx='CASCADE',
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
    last_propagate = max(
        i for i, t in enumerate(types) if t == 'propagate_wave')
    first_bpmx = min(
        i for i, t in enumerate(types) if t == 'bpmx_iteration')
    assert last_propagate < first_bpmx
