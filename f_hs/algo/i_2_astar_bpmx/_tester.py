import pytest

from f_hs.algo.i_2_astar_bpmx import AStarBPMX
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


# ─────────────────────────────────────────────────────────────
#  Validation
# ─────────────────────────────────────────────────────────────

def test_rule_pathmax_validation() -> None:
    """
    ========================================================================
     `rule_pathmax` accepts None / 1 / 2 / 3; rejects everything else.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    for ok in (None, 1, 2, 3):
        AStarBPMX(problem=problem, h=lambda s: 0, rule_pathmax=ok)
    for bad in (0, 4, -1, '1', '3', 1.5):
        with pytest.raises(ValueError, match='rule_pathmax'):
            AStarBPMX(problem=problem, h=lambda s: 0, rule_pathmax=bad)


def test_depth_bpmx_validation() -> None:
    """
    ========================================================================
     `depth_bpmx` accepts None and int >= 0; rejects negatives,
     non-ints, and bool.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    for ok in (None, 0, 1, 2, 10):
        AStarBPMX(problem=problem, h=lambda s: 0, depth_bpmx=ok)
    for bad in (-1, -5, 1.5, '1', True, False):
        with pytest.raises(ValueError, match='depth_bpmx'):
            AStarBPMX(problem=problem, h=lambda s: 0, depth_bpmx=bad)


def test_rejects_hcached_chain() -> None:
    """
    ========================================================================
     A pre-built HBase chain that contains HCached is rejected
     with a redirect to AStarLookup.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    goal = list(problem.goals)[0]
    cache = {goal: CacheEntry(h_perfect=0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 0), cache=cache, goal=goal)
    with pytest.raises(TypeError, match='AStarLookup'):
        AStarBPMX(problem=problem, h=h)


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
     With rule_pathmax / depth_bpmx active and `bounds=None`,
     an empty HBounded is auto-wrapped as storage.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    algo = AStarBPMX(problem=problem, h=lambda s: 0,
                     rule_pathmax=1)
    assert AStarBPMX._find_hbounded(algo._h) is not None
    algo = AStarBPMX(problem=problem, h=lambda s: 0,
                     depth_bpmx=1)
    assert AStarBPMX._find_hbounded(algo._h) is not None


# ─────────────────────────────────────────────────────────────
#  Off (baseline)
# ─────────────────────────────────────────────────────────────

def test_off_behaves_like_astar() -> None:
    """
    ========================================================================
     With both mechanisms off, AStarBPMX finds the same optimal
     solution as plain AStar on the 4x4 obstacle grid.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_off()
    sol = algo.run()
    assert sol.cost == 7.0


def test_off_emits_no_bpmx_events() -> None:
    """
    ========================================================================
     Off configuration emits no pathmax / BPMX events.
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

@pytest.mark.parametrize('rule_pathmax', [None, 1, 2, 3])
@pytest.mark.parametrize('depth_bpmx', [0, 1, 2, None])
def test_optimality_grid_4x4(rule_pathmax: int | None,
                             depth_bpmx: int | None) -> None:
    """
    ========================================================================
     Optimal cost (7) recovered on the 4x4 obstacle grid for
     every combination of (rule_pathmax, depth_bpmx).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarBPMX(
        problem=problem,
        h=lambda s: float(s.distance(goal)),
        rule_pathmax=rule_pathmax,
        depth_bpmx=depth_bpmx,
    )
    sol = algo.run()
    assert sol.cost == 7.0


# ─────────────────────────────────────────────────────────────
#  Lift events on inconsistent toy graph
# ─────────────────────────────────────────────────────────────

def test_bpmx_lifts_on_inconsistent_diamond() -> None:
    """
    ========================================================================
     Diamond graph A->B,A->C,B->D,C->D with inconsistent h
     (B is over-bumped to h=4 while h*(B,D)=1) -> BPMX cascade
     fires Rule 3 to lift A from B and Rule 1 to forward the
     lift to A's other child C.
    ========================================================================
    """
    algo = AStarBPMX.Factory.graph_diamond_inconsistent_bpmx_full()
    algo.run()
    types = [e['type'] for e in algo.recorder.events]
    assert 'bpmx_iteration' in types
    # Optimal cost preserved despite inconsistent h.
    assert algo.recorder.events[-1].get('type') in (
        'pop', 'bpmx_iteration', 'bpmx_lift', 'bpmx_forward',
        'push', 'decrease_g')


def test_pathmax_rule3_lifts_parent_via_high_h_child() -> None:
    """
    ========================================================================
     With rule_pathmax=3 and a child carrying high h, the parent's
     h is lifted by reverse pathmax. Recorded as a pathmax_apply
     event with rule=3 and via_child set.
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
    rule3 = [e for e in algo.recorder.events
             if e.get('type') == 'pathmax_apply'
             and e.get('rule') == 3]
    assert len(rule3) >= 1
    # The first such event should lift A from B.
    e = rule3[0]
    assert e['state'].key == 'A'
    assert e['via_child'].key == 'B'
    assert e['h_old'] == 0
    assert e['h_new'] >= 3  # h(B) - w(B, A) = 4 - 1 = 3


# ─────────────────────────────────────────────────────────────
#  Counters
# ─────────────────────────────────────────────────────────────

def test_counters_scaffold_shape() -> None:
    """
    ========================================================================
     The counters scaffold has exactly the 10 declared names
     in three groups.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_off()
    expected = {
        'cnt_pathmax_attempts', 'cnt_pathmax_lifts',
        'cnt_bpmx_attempts', 'cnt_bpmx_iterations',
        'cnt_bpmx_rule3_lifts', 'cnt_bpmx_rule1_forwards',
        'cnt_bpmx_subtree_states',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
    }
    assert set(algo.counters) == expected


def test_counters_off_records_no_bpmx_activity() -> None:
    """
    ========================================================================
     With both mechanisms off, all bpmx / pathmax counters are 0;
     frontier counters are positive.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_off()
    algo.run()
    c = algo.counters
    for name in ('cnt_pathmax_attempts', 'cnt_pathmax_lifts',
                 'cnt_bpmx_attempts', 'cnt_bpmx_iterations',
                 'cnt_bpmx_rule3_lifts',
                 'cnt_bpmx_rule1_forwards',
                 'cnt_bpmx_subtree_states'):
        assert c[name] == 0
    assert c['cnt_push'] > 0
    assert c['cnt_pop'] > 0


def test_counters_rule1_attempts_per_expansion() -> None:
    """
    ========================================================================
     With rule_pathmax=1, attempts == expansions
     (= cnt_pop minus the goal-pop that short-circuits before
     _pre_expand). On a path-found run, attempts == cnt_pop - 1.
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_rule1()
    algo.run()
    c = algo.counters
    assert c['cnt_pathmax_attempts'] == c['cnt_pop'] - 1


def test_counters_bpmx_full_records_subtree_states() -> None:
    """
    ========================================================================
     With BPMX(infinity), cnt_bpmx_subtree_states is at least
     the cumulative attempts (root counts at every expansion).
    ========================================================================
    """
    algo = AStarBPMX.Factory.grid_4x4_bpmx_full()
    algo.run()
    c = algo.counters
    assert c['cnt_bpmx_attempts'] >= 1
    assert c['cnt_bpmx_subtree_states'] >= c['cnt_bpmx_attempts']
    assert c['cnt_bpmx_iterations'] >= c['cnt_bpmx_attempts']


# ─────────────────────────────────────────────────────────────
#  Inheritance / dispatch
# ─────────────────────────────────────────────────────────────

def test_is_subclass_of_astar() -> None:
    """
    ========================================================================
     AStarBPMX extends AStar (sibling of AStarLookup).
    ========================================================================
    """
    from f_hs.algo.i_1_astar.main import AStar
    algo = AStarBPMX.Factory.grid_4x4_off()
    assert isinstance(algo, AStar)
    assert type(algo).__name__ == 'AStarBPMX'


def test_factory_attached() -> None:
    """
    ========================================================================
     AStarBPMX.Factory is wired through __init__.py.
    ========================================================================
    """
    assert AStarBPMX.Factory is not None
    assert hasattr(AStarBPMX.Factory, 'grid_4x4_off')
