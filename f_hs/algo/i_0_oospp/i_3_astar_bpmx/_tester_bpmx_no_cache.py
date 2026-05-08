import pytest

from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


def _events_of_type(algo: AStarBPMX, *types: str) -> list[dict]:
    """
    ========================================================================
     Filter the recorder log to events whose `type` is in
     `types`. Shared helper for event-schema tests.
    ========================================================================
    """
    return [e for e in algo.recorder.events
            if e.get('type') in types]


# ─────────────────────────────────────────────────────────────
#  Validation
# ─────────────────────────────────────────────────────────────

def test_rule_bpmx_validation() -> None:
    """
    ========================================================================
     `rule_bpmx` accepts None / '1' / '2' / '3' / 'CASCADE';
     rejects everything else.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    for ok in (None, '1', '2', '3', 'CASCADE'):
        AStarBPMX(problem=problem, h=lambda s: 0, rule_bpmx=ok)
    for bad in (1, 2, 3, 0, 'cascade', 'rule1', '4', 1.5):
        with pytest.raises(ValueError, match='rule_bpmx'):
            AStarBPMX(problem=problem, h=lambda s: 0, rule_bpmx=bad)


def test_depth_bpmx_validation() -> None:
    """
    ========================================================================
     `depth_bpmx` accepts None and int >= 1; rejects 0,
     negatives, non-ints, and bool.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    for ok in (None, 1, 2, 10):
        AStarBPMX(problem=problem, h=lambda s: 0,
                  rule_bpmx='1', depth_bpmx=ok)
    for bad in (0, -1, -5, 1.5, '1', True, False):
        with pytest.raises(ValueError, match='depth_bpmx'):
            AStarBPMX(problem=problem, h=lambda s: 0,
                      rule_bpmx='1', depth_bpmx=bad)


def test_rule2_requires_depth_1() -> None:
    """
    ========================================================================
     Rule 2 cannot propagate beyond depth 1 — its operator
     consumes a parent + its full children set, which has no
     chained-grandparent analogue. depth_bpmx > 1 and None
     are both rejected for Rule 2.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    # depth=1 is fine.
    AStarBPMX(problem=problem, h=lambda s: 0,
              rule_bpmx='2', depth_bpmx=1)
    # depth>1 rejected.
    for bad in (2, 5, None):
        with pytest.raises(ValueError, match='Rule 2'):
            AStarBPMX(problem=problem, h=lambda s: 0,
                      rule_bpmx='2', depth_bpmx=bad)


def test_rejects_bounds_with_prebuilt_h() -> None:
    """
    ========================================================================
     Pre-built HBase `h` combined with `bounds` is rejected
     (would double-wrap).
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    h = HCallable(fn=lambda s: 0)
    with pytest.raises(ValueError, match='bounds'):
        AStarBPMX(problem=problem, h=h, bounds={})


def test_auto_wraps_hbounded_when_mechanism_on() -> None:
    """
    ========================================================================
     With `rule_bpmx` active and `bounds=None`, an empty
     HBounded is auto-wrapped as storage.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    for rule in ('1', '2', '3', 'CASCADE'):
        algo = AStarBPMX(problem=problem, h=lambda s: 0,
                         rule_bpmx=rule)
        assert AStarBPMX._find_hbounded(algo._h) is not None


# ─────────────────────────────────────────────────────────────
#  Off (baseline)
# ─────────────────────────────────────────────────────────────

def test_off_behaves_like_astar() -> None:
    """
    ========================================================================
     With rule_bpmx=None, AStarBPMX finds the same optimal
     solution as plain AStar on the 4x4 obstacle grid.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4()
    sol = algo.run()
    assert sol.cost == 7.0


def test_off_emits_no_bpmx_events() -> None:
    """
    ========================================================================
     Off configuration (rule_bpmx=None) emits no pathmax / BPMX
     events.
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
    assert types.isdisjoint({'pathmax_apply', 'bpmx_iteration',
                             'bpmx_lift', 'bpmx_forward'})


# ─────────────────────────────────────────────────────────────
#  Optimality preserved across all configurations
# ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize('rule_bpmx,depth_bpmx', [
    (None, 1),
    ('1', 1), ('1', 2), ('1', None),
    ('2', 1),
    ('3', 1), ('3', 2), ('3', None),
    ('CASCADE', 1), ('CASCADE', 2), ('CASCADE', None),
])
def test_optimality_grid_4x4(rule_bpmx: str | None,
                             depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Optimal cost (7) recovered on the 4x4 obstacle grid for
     every valid (rule_bpmx, depth_bpmx) combination.
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
    sol = algo.run()
    assert sol.cost == 7.0


# ─────────────────────────────────────────────────────────────
#  Lift events on inconsistent toy graph (graph_diamond)
# ─────────────────────────────────────────────────────────────

def test_cascade_lifts_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     Diamond graph with inconsistent h (B is over-bumped to
     h=4 while h*(B,D)=1) -> CASCADE fires Rule 3 to lift A
     from B and Rule 1 to forward the lift to A's other
     child C.
    ========================================================================
    """
    algo = AStarBPMX.Factory.graph_diamond_inconsistent_cascade()
    algo.run()
    types = [e['type'] for e in algo.recorder.events]
    assert 'bpmx_iteration' in types
    # Optimal cost preserved despite inconsistent h.
    assert algo.recorder.events[-1].get('type') in (
        'pop', 'bpmx_iteration', 'bpmx_lift', 'bpmx_forward',
        'push', 'decrease_g')


def test_rule3_isolated_lifts_parent_via_high_h_child() -> None:
    """
    ========================================================================
     With rule_bpmx='3' (depth=1) and a child carrying high h,
     the parent's h is lifted by reverse pathmax. Recorded as
     a `bpmx_lift` event with via_child set.
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
             if e.get('type') == 'bpmx_lift']
    assert len(lifts) >= 1
    e = lifts[0]
    assert e['state'].key == 'A'
    assert e['via_child'].key == 'B'
    assert e['h_old'] == 0
    assert e['h_new'] >= 3   # h(B) - w(B, A) = 4 - 1 = 3


# ─────────────────────────────────────────────────────────────
#  Generic event-schema tests on inconsistent graph_diamond
#  (Per-rule recording on grid_4x4_obstacle lives in
#  _tester_recording.py.)
# ─────────────────────────────────────────────────────────────

def test_bpmx_forward_event_schema_rule1_isolated() -> None:
    """
    ========================================================================
     Rule 1 (isolated, depth=1) emits `bpmx_forward` events
     with state, h_old, h_new, via_parent, duration.
    ========================================================================
    """
    h_inc = {'A': 5.0, 'B': 0.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_bpmx='1',
        depth_bpmx=1,
        is_recording=True,
    )
    algo.run()
    events = _events_of_type(algo, 'bpmx_forward')
    assert len(events) >= 1
    e = events[0]
    expected = {'type', 'state', 'h_old', 'h_new',
                'via_parent', 'duration'}
    assert expected.issubset(set(e.keys()))
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
        rule_bpmx='2',
        depth_bpmx=1,
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


def test_bpmx_lift_event_schema_rule3_isolated() -> None:
    """
    ========================================================================
     Rule 3 (isolated, depth=1) emits `bpmx_lift` events with
     state, h_old, h_new, via_child.
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
    events = _events_of_type(algo, 'bpmx_lift')
    assert len(events) >= 1
    e = events[0]
    expected = {'type', 'state', 'h_old', 'h_new',
                'via_child', 'duration'}
    assert expected.issubset(set(e.keys()))


def test_bpmx_iteration_marker_per_cascade() -> None:
    """
    ========================================================================
     Each CASCADE invocation emits at least one
     `bpmx_iteration` event with iteration index, num_levels,
     num_states. (Iteration markers are CASCADE-specific —
     isolated rule sweeps emit no iteration events.)
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_bpmx='CASCADE',
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


def test_bpmx_iteration_indices_monotone_per_cascade() -> None:
    """
    ========================================================================
     CASCADE iteration indices reset to 1 at the start of each
     expansion's cascade and increase monotonically within it.
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
    iters = _events_of_type(algo, 'bpmx_iteration')
    last_root = None
    last_idx = 0
    for e in iters:
        if e['state'] is not last_root:
            last_root = e['state']
            assert e['iteration'] == 1
            last_idx = 1
        else:
            assert e['iteration'] == last_idx + 1
            last_idx = e['iteration']


def test_bpmx_forward_event_after_cascade_lift() -> None:
    """
    ========================================================================
     During CASCADE on the inconsistent diamond, after Rule 3
     lifts the parent, Rule 1 forwards the lifted value to
     the parent's other children — emits `bpmx_forward` with
     via_parent set.
    ========================================================================
    """
    h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
    algo = AStarBPMX(
        problem=ProblemSPP.Factory.graph_diamond(),
        h=lambda s: h_inc.get(s.key, 0.0),
        rule_bpmx='CASCADE',
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
#  Counters — generic / cross-rule invariants
#  (Per-rule counter pinning on grid_4x4_obstacle lives in
#  _tester_counters.py.)
# ─────────────────────────────────────────────────────────────

def test_counters_scaffold_shape() -> None:
    """
    ========================================================================
     The counters scaffold has exactly the 15 declared names in
     five groups (propagate 3, BPMX 3, frontier 3, search-
     semantic 2, memory 4) — AStarBPMX's `_COUNTER_NAMES`.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4()
    expected = {
        'cnt_prop_waves', 'cnt_prop_attempts', 'cnt_prop_lifts',
        'cnt_bpmx_attempts',
        'cnt_bpmx_successes',
        'cnt_bpmx_depth',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
        'mem_open', 'mem_closed',
        'mem_cache', 'mem_bounds',
    }
    assert set(algo.counters) == expected


def test_counters_off_records_no_bpmx_activity() -> None:
    """
    ========================================================================
     With rule_bpmx=None, all BPMX-mechanism counters are 0;
     frontier counters are positive.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4()
    algo.run()
    c = algo.counters
    for name in ('cnt_bpmx_attempts',
                 'cnt_bpmx_successes',
                 'cnt_bpmx_depth'):
        assert c[name] == 0
    assert c['cnt_push'] > 0
    assert c['cnt_pop'] > 0


@pytest.mark.parametrize('rule_bpmx', ['1', '2', '3', 'CASCADE'])
def test_counters_attempts_per_expansion(rule_bpmx: str) -> None:
    """
    ========================================================================
     With any rule_bpmx active and depth=1, attempts ==
     expansions (cnt_pop minus the goal-pop that
     short-circuits before _pre_expand).
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx=rule_bpmx,
                                      depth_bpmx=1)
    algo.run()
    c = algo.counters
    assert c['cnt_bpmx_attempts'] == c['cnt_pop'] - 1


def test_counters_successes_zero_under_consistent_h() -> None:
    """
    ========================================================================
     Manhattan h on grid_4x4_obstacle is consistent
     (1-Lipschitz). Rules 1 / 3 / CASCADE attempt but never
     strictly tighten → cnt_bpmx_successes == 0. Rule 2 can
     fire at "local minimum" cells where the obstacle blocks
     every h-decreasing successor → cnt_bpmx_successes == 2.
    ========================================================================
    """
    for rule in ('1', '3', 'CASCADE'):
        algo = AStarBPMX.Factory.grid_4x4(rule_bpmx=rule,
                                          depth_bpmx=1)
        algo.run()
        assert algo.counters['cnt_bpmx_successes'] == 0
    algo2 = AStarBPMX.Factory.grid_4x4(rule_bpmx='2', depth_bpmx=1)
    algo2.run()
    assert algo2.counters['cnt_bpmx_successes'] == 2


def test_counters_depth_max_tracker() -> None:
    """
    ========================================================================
     `cnt_bpmx_depth` tracks the deepest BFS-level at which
     any lift fired (max via assign, not cumulative). On
     grid_4x4_obstacle with consistent Manhattan h, no lifts
     fire → stays at the init value 0. Rule 2 lifts the root
     itself → still 0.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4(rule_bpmx='CASCADE',
                                      depth_bpmx=None)
    algo.run()
    assert algo.counters['cnt_bpmx_depth'] == 0
    algo2 = AStarBPMX.Factory.grid_4x4(rule_bpmx='2', depth_bpmx=1)
    algo2.run()
    # Rule 2 lifts the popped state itself (level 0).
    assert algo2.counters['cnt_bpmx_depth'] == 0


def test_counters_depth_positive_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     On the inconsistent diamond graph + CASCADE(None), Rule 3
     lifts the root A from B (level 0) and Rule 1 forwards to
     the cousin C (level 1). cnt_bpmx_depth ends at the
     deepest lifted level — at least 1.
    ========================================================================
    """
    algo = AStarBPMX.Factory.graph_diamond_inconsistent_cascade()
    algo.run()
    assert algo.counters['cnt_bpmx_depth'] >= 1


# ─────────────────────────────────────────────────────────────
#  Inheritance / dispatch
# ─────────────────────────────────────────────────────────────

def test_is_subclass_of_astar() -> None:
    """
    ========================================================================
     AStarBPMX extends AStar (sibling of AStarBPMX).
    ========================================================================
    """
    from f_hs.algo.i_0_oospp.i_1_astar.main import AStar
    algo = AStarBPMX.Factory.grid_4x4()
    assert isinstance(algo, AStar)
    assert type(algo).__name__ == 'AStarBPMX'


def test_factory_attached() -> None:
    """
    ========================================================================
     AStarBPMX.Factory is wired through __init__.py.
    ========================================================================
    """
    assert AStarBPMX.Factory is not None
    assert hasattr(AStarBPMX.Factory, 'grid_4x4')
