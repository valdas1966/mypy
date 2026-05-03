from f_hs.algo.i_2_astar_bpmx import AStarBPMX
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


# ─────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────

def _events_of_type(algo: AStarBPMX, *types: str) -> list[dict]:
    return [e for e in algo.recorder.events
            if e.get('type') in types]


# ─────────────────────────────────────────────────────────────
#  pathmax_apply events
# ─────────────────────────────────────────────────────────────

def test_pathmax_apply_rule1_event_schema() -> None:
    """
    ========================================================================
     Rule 1 emits pathmax_apply events with state, rule=1,
     h_old, h_new, via_parent, duration.
    ========================================================================
    """
    h_inc = {'A': 5.0, 'B': 0.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_pathmax=1,
        depth_bpmx=0,
        is_recording=True,
    )
    algo.run()
    events = _events_of_type(algo, 'pathmax_apply')
    assert len(events) >= 1
    e = events[0]
    expected = {'type', 'state', 'rule', 'h_old', 'h_new',
                'via_parent', 'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['rule'] == 1
    assert isinstance(e['h_old'], int)
    assert isinstance(e['h_new'], int)
    assert e['h_new'] > e['h_old']


def test_pathmax_apply_rule2_event_schema() -> None:
    """
    ========================================================================
     Rule 2 emits pathmax_apply events with state, rule=2,
     h_old, h_new, via_children (tuple).
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 3.0, 'C': 3.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_pathmax=2,
        depth_bpmx=0,
        is_recording=True,
    )
    algo.run()
    events = _events_of_type(algo, 'pathmax_apply')
    rule2 = [e for e in events if e.get('rule') == 2]
    assert len(rule2) >= 1
    e = rule2[0]
    expected = {'type', 'state', 'rule', 'h_old', 'h_new',
                'via_children', 'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['rule'] == 2
    assert isinstance(e['via_children'], tuple)


def test_pathmax_apply_rule3_event_schema() -> None:
    """
    ========================================================================
     Rule 3 emits pathmax_apply events with state, rule=3,
     h_old, h_new, via_child.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_pathmax=3,
        depth_bpmx=0,
        is_recording=True,
    )
    algo.run()
    events = _events_of_type(algo, 'pathmax_apply')
    rule3 = [e for e in events if e.get('rule') == 3]
    assert len(rule3) >= 1
    e = rule3[0]
    expected = {'type', 'state', 'rule', 'h_old', 'h_new',
                'via_child', 'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['rule'] == 3


# ─────────────────────────────────────────────────────────────
#  bpmx_iteration meta-event
# ─────────────────────────────────────────────────────────────

def test_bpmx_iteration_marker_per_expansion() -> None:
    """
    ========================================================================
     Each expansion emits at least one bpmx_iteration event with
     iteration index, num_levels, num_states.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        depth_bpmx=1,
        is_recording=True,
    )
    algo.run()
    iters = _events_of_type(algo, 'bpmx_iteration')
    assert len(iters) >= 1
    e = iters[0]
    expected = {'type', 'state', 'iteration', 'num_levels',
                'num_states', 'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['iteration'] >= 1
    assert e['num_levels'] >= 1
    assert e['num_states'] >= 1


def test_bpmx_iteration_indices_monotone_per_expansion() -> None:
    """
    ========================================================================
     Iteration indices reset to 1 at the start of each
     expansion's BPMX cascade and increase monotonically within
     it.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    iters = _events_of_type(algo, 'bpmx_iteration')
    # Group iteration sequences by the expansion's root state.
    last_root = None
    last_idx = 0
    for e in iters:
        if e['state'] is not last_root:
            last_root = e['state']
            assert e['iteration'] == 1, (
                f'first iter for new root must be 1, got '
                f'{e["iteration"]}')
            last_idx = 1
        else:
            assert e['iteration'] == last_idx + 1
            last_idx = e['iteration']


# ─────────────────────────────────────────────────────────────
#  bpmx_lift / bpmx_forward
# ─────────────────────────────────────────────────────────────

def test_bpmx_lift_event_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     On the diamond graph with B's h artificially raised, BPMX
     fires Rule 3 and emits a bpmx_lift event for the parent
     A with via_child=B.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    lifts = _events_of_type(algo, 'bpmx_lift')
    assert len(lifts) >= 1
    e = lifts[0]
    expected = {'type', 'state', 'h_old', 'h_new', 'via_child',
                'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['state'].key == 'A'
    assert e['via_child'].key == 'B'
    assert e['h_new'] > e['h_old']


def test_bpmx_forward_event_after_lift() -> None:
    """
    ========================================================================
     After Rule 3 lifts a parent, Rule 1 forwards the lifted
     value to the parent's other children -- emits a
     bpmx_forward event with via_parent set.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        depth_bpmx=None,
        is_recording=True,
    )
    algo.run()
    forwards = _events_of_type(algo, 'bpmx_forward')
    assert len(forwards) >= 1
    e = forwards[0]
    expected = {'type', 'state', 'h_old', 'h_new', 'via_parent',
                'duration'}
    assert expected.issubset(set(e.keys()))
    assert e['h_new'] > e['h_old']
    assert isinstance(e['h_old'], int)
    assert isinstance(e['h_new'], int)


# ─────────────────────────────────────────────────────────────
#  Off configuration emits no BPMX/pathmax events
# ─────────────────────────────────────────────────────────────

def test_off_emits_only_search_events() -> None:
    """
    ========================================================================
     With both mechanisms off, only standard AStar push / pop /
     decrease_g events appear.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        is_recording=True,
    )
    algo.run()
    types = {e['type'] for e in algo.recorder.events}
    assert types <= {'push', 'pop', 'decrease_g'}
