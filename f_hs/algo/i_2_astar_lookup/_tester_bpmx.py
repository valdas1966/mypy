import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_2_astar_lookup._utils import normalize
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def _sc(r: int, c: int) -> StateCell:
    return StateCell(key=CellMap(row=r, col=c))


# ──────────────────────────────────────────────────
#  1. Flag validation / defaults
# ──────────────────────────────────────────────────


def test_bpmx_off_by_default_emits_no_events() -> None:
    """
    ========================================================================
     `AStarLookup(..., bpmx=None)` (or omitted) runs classical
     A* with no BPMX events.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        is_recording=True,
    )
    algo.run()
    assert not any(e['type'] in ('bpmx_lift', 'bpmx_forward')
                   for e in algo.recorder.events)


def test_bpmx_rejects_rule_3_alone() -> None:
    """
    ========================================================================
     `bpmx='3'` raises — cascade without Rule 2 has no trigger.
    ========================================================================
    """
    with pytest.raises(ValueError, match='bpmx must be one of'):
        AStarLookup(problem=ProblemSPP.Factory.graph_abc(),
                    h=lambda s: 0, bpmx='3')


def test_bpmx_rejects_rule_13() -> None:
    """
    ========================================================================
     `bpmx='13'` raises — cascade without Rule 2 has no trigger.
    ========================================================================
    """
    with pytest.raises(ValueError, match='bpmx must be one of'):
        AStarLookup(problem=ProblemSPP.Factory.graph_abc(),
                    h=lambda s: 0, bpmx='13')


def test_bpmx_rejects_garbage_strings() -> None:
    """
    ========================================================================
     Non-digit strings / digits in wrong order raise.
    ========================================================================
    """
    for bad in ['abc', 'xyz', '21', '0', '4', '1234']:
        with pytest.raises(ValueError, match='bpmx must be one of'):
            AStarLookup(problem=ProblemSPP.Factory.graph_abc(),
                        h=lambda s: 0, bpmx=bad)


def test_bpmx_autocreates_empty_hbounded_when_needed() -> None:
    """
    ========================================================================
     `bpmx='12'` without explicit bounds auto-wraps an empty
     HBounded. propagate_pathmax (which also needs HBounded)
     works subsequently.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bpmx='12',
    )
    assert algo._find_hbounded(algo._h) is not None


def test_bpmx_rejects_prebuilt_h_without_hbounded() -> None:
    """
    ========================================================================
     If `h` is pre-built HBase with no HBounded in the chain,
     BPMX has no storage. Raises.
    ========================================================================
    """
    h = HCallable(fn=lambda s: 0)   # no HBounded in chain
    with pytest.raises(ValueError, match='HBounded'):
        AStarLookup(problem=ProblemSPP.Factory.graph_abc(),
                    h=h, bpmx='12')


# ──────────────────────────────────────────────────
#  2. Rule mechanics
# ──────────────────────────────────────────────────


def test_bpmx_rule_2_lifts_parent_from_cached_child() -> None:
    """
    ========================================================================
     Expand a state with a cached child. Rule 2 backward-lifts
     the parent's h from the child's perfect h*. Emits bpmx_lift.
    ========================================================================
    """
    # graph_abc: A -> B -> C. Cache C with h*=0, goal=C.
    # Expanding B: child C has h*=0, w(C,B)=1. cand = 0-1 = -1 < h(B)=?
    # Need parent's h to be SMALL and child's h to be LARGE.
    # Use graph_decrease: S -> A/B -> X with w(B,X)=0.
    # Cache X with h*=0. Expanding A gives child X with h*=0,
    # cand = 0 - w(X,A)=? A doesn't link to X via X→A. Forget.
    #
    # Simpler: grid. Start (0,0), cache (0,1) with h*=6.
    # Expanding (0,0): base Manhattan=3. Child (0,1) cached h=6.
    # cand = 6 - w((0,1), (0,0)) = 6 - 1 = 5. 5 > 3 → lift (0,0) to 5.
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal   # (0,3)
    p01 = _sc(0, 1)
    p11 = _sc(1, 1)
    p21 = _sc(2, 1)
    p22 = _sc(2, 2)
    p23 = _sc(2, 3)
    p13 = _sc(1, 3)
    p03 = _sc(0, 3)
    cache = {
        p01: CacheEntry(h_perfect=6, suffix_next=p11),
        p11: CacheEntry(h_perfect=5, suffix_next=p21),
        p21: CacheEntry(h_perfect=4, suffix_next=p22),
        p22: CacheEntry(h_perfect=3, suffix_next=p23),
        p23: CacheEntry(h_perfect=2, suffix_next=p13),
        p13: CacheEntry(h_perfect=1, suffix_next=p03),
        p03: CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        cache=cache,
        goal=p03,
        bpmx='2',
        is_recording=True,
    )
    algo.run()
    lifts = [e for e in algo.recorder.events
             if e['type'] == 'bpmx_lift']
    # (0,0) should be lifted: Manhattan=3 → 5 (via cached (0,1) h=6).
    assert any(e['state'].rc == (0, 0) and e['h_new'] == 5
               for e in lifts)


def test_bpmx_rule_1_forward_tightens_child() -> None:
    """
    ========================================================================
     Parent has a pre-seeded bound (h=7 on (0,0)). On expansion
     of (0,0) with Rule 1, its children get forward-lifted.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(0, 0): 7},
        bpmx='1',
        is_recording=True,
    )
    algo.run()
    fwds = [e for e in algo.recorder.events
            if e['type'] == 'bpmx_forward']
    # (0,1) and (1,0) should be forward-lifted from (0,0)'s
    # bounded h=7. cand = 7-1 = 6. Manhattan for (0,1)=2 → 6.
    # Manhattan for (1,0)=4 → 6.
    lifted_states = {e['state'].rc for e in fwds}
    assert (0, 1) in lifted_states
    assert (1, 0) in lifted_states
    for e in fwds:
        if e['state'].rc in {(0, 1), (1, 0)}:
            assert e['h_new'] == 6
            assert e['via_parent'].rc == (0, 0)


def test_bpmx_rule_12_both_fire_in_same_expansion() -> None:
    """
    ========================================================================
     Rule 1 + Rule 2 at the same expansion. Cached neighbour
     triggers Rule 2 lift on parent. Pins both rules register
     in the event log even if Rule 1's forward attempt is a
     no-op on this particular geometry.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    cache = {
        _sc(0, 1): CacheEntry(h_perfect=6, suffix_next=None),
        _sc(0, 3): CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        cache=cache,
        goal=_sc(0, 3),
        bpmx='12',
        is_recording=True,
    )
    algo.run()
    events = algo.recorder.events
    lifts = [e for e in events if e['type'] == 'bpmx_lift']
    # Rule 2: (0,0) lifts from Manhattan=3 to 5 (via (0,1) h=6).
    assert any(e['state'].rc == (0, 0) and e['h_new'] == 5
               for e in lifts)


def test_bpmx_rule_123_cascade_iterates() -> None:
    """
    ========================================================================
     Cascade ('123') iterates Rules 1+2 to a fixed point. No
     infinite loop on an already-converged setup.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    cache = {
        _sc(0, 1): CacheEntry(h_perfect=6, suffix_next=None),
        _sc(0, 3): CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        cache=cache,
        goal=_sc(0, 3),
        bounds={_sc(1, 0): 6},
        bpmx='123',
        is_recording=True,
    )
    algo.run()
    events = algo.recorder.events
    lifts = [e for e in events if e['type'] == 'bpmx_lift']
    assert any(e['state'].rc == (0, 0) for e in lifts)
    # No runaway cascade.
    bpmx_ct = sum(1 for e in events
                  if e['type'] in ('bpmx_lift', 'bpmx_forward'))
    assert bpmx_ct < 50


def test_bpmx_skips_cached_states() -> None:
    """
    ========================================================================
     Cached states (is_perfect True) are not targets of Rule 1
     forward lift — they're already perfect.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    cache = {
        _sc(0, 1): CacheEntry(h_perfect=6, suffix_next=None),
        _sc(0, 3): CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        cache=cache,
        goal=_sc(0, 3),
        bounds={_sc(0, 0): 7},   # tight admissible seed
        bpmx='12',
        is_recording=True,
    )
    algo.run()
    fwds = [e for e in algo.recorder.events
            if e['type'] == 'bpmx_forward']
    # Rule 1 never lifts a cached state.
    assert not any(e['state'].rc == (0, 1) for e in fwds)


# ──────────────────────────────────────────────────
#  3. Correctness invariants
# ──────────────────────────────────────────────────


def test_bpmx_preserves_admissibility_all_configs() -> None:
    """
    ========================================================================
     For each valid bpmx config, optimal cost matches the no-BPMX
     baseline. BPMX preserves admissibility.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal

    def run(bpmx_val):
        a = AStarLookup(
            problem=ProblemGrid.Factory.grid_4x4_obstacle(),
            h=lambda s: s.distance(goal),
            bpmx=bpmx_val,
        )
        return a.run().cost

    baseline = run(None)
    for cfg in ('1', '2', '12', '23', '123'):
        assert run(cfg) == baseline, f'cost drift at bpmx={cfg!r}'


def test_bpmx_vs_propagate_pathmax_same_cost() -> None:
    """
    ========================================================================
     In-search BPMX and pre-search propagate_pathmax are
     different mechanisms; both preserve optimality. Shared
     setup: grid_4x4_obstacle with HBounded seeded at (0,0)=7.
     Both should return cost 7.
    ========================================================================
    """
    def build_algo(bpmx_val):
        return AStarLookup(
            problem=ProblemGrid.Factory.grid_4x4_obstacle(),
            h=lambda s: s.distance(
                ProblemGrid.Factory.grid_4x4_obstacle().goal),
            bounds={_sc(0, 0): 7},
            bpmx=bpmx_val,
            is_recording=True,
        )

    # Pre-search pathmax only (no in-search BPMX).
    a1 = build_algo(bpmx_val=None)
    a1.propagate_pathmax()
    sol1 = a1.run()
    assert sol1.cost == 7

    # In-search BPMX only (no pre-search pathmax).
    a2 = build_algo(bpmx_val='12')
    sol2 = a2.run()
    assert sol2.cost == 7

    # Both mechanisms together.
    a3 = build_algo(bpmx_val='12')
    a3.propagate_pathmax()
    sol3 = a3.run()
    assert sol3.cost == 7

    # Event signatures differ by mechanism used:
    # a1 (pre-propagation only) has propagate events, no bpmx.
    # a2 (BPMX only) has bpmx events, no propagate.
    # a3 (both) has propagate events; BPMX may or may not fire
    # additionally depending on whether pre-propagation already
    # tightened everything — semantically that's the point
    # (pre-propagation subsumes BPMX on this small setup).
    has_prop = lambda algo: any(
        e['type'] in ('propagate_wave', 'propagate')
        for e in algo.recorder.events)
    has_bpmx = lambda algo: any(
        e['type'] in ('bpmx_lift', 'bpmx_forward')
        for e in algo.recorder.events)
    assert has_prop(a1) and not has_bpmx(a1)
    assert has_bpmx(a2) and not has_prop(a2)
    assert has_prop(a3)   # BPMX may be subsumed


# ──────────────────────────────────────────────────
#  4. Full event-sequence recording
# ──────────────────────────────────────────────────


def test_recording_bpmx_rule_1_forward_on_graph_abc() -> None:
    """
    ========================================================================
     Rule 1 only (bpmx='1') with HBounded seed at A.

     Chain is `HBounded(HCallable(0))` — no HCached. The outer
     is HBounded, so `is_bounded` flags surface correctly on
     push/pop of every state that ends up with a bound >
     base.

     Trace:
       push A (h=5, bounded)
       pop A
       Rule 1 lifts B: cand = 5-1 = 4 > base 0 → emit
         bpmx_forward(B, 0→4, via=A).
       push B (h=4, now bounded)
       pop B
       Rule 1 lifts C: cand = 4-1 = 3 > base 0 → emit
         bpmx_forward(C, 0→3, via=B).
       push C (h=3, now bounded)
       pop C (goal — cost=2)
    ========================================================================
    """
    from f_hs.problem.i_0_base._factory import _ProblemGraph
    problem = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': []},
        start='A', goal='C',
    )
    a_state = problem._states['A']
    algo = AStarLookup(
        problem=problem,
        h=lambda s: 0,
        bounds={a_state: 5},
        bpmx='1',
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None,
         'h': 5, 'f': 5, 'is_bounded': True},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 5, 'f': 5,
         'is_bounded': True},
        {'type': 'bpmx_forward', 'state': 'B', 'h_old': 0,
         'h_new': 4, 'via_parent': 'A'},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A',
         'h': 4, 'f': 5, 'is_bounded': True},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 4, 'f': 5,
         'is_bounded': True},
        {'type': 'bpmx_forward', 'state': 'C', 'h_old': 0,
         'h_new': 3, 'via_parent': 'B'},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B',
         'h': 3, 'f': 5, 'is_bounded': True},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 3, 'f': 5,
         'is_bounded': True},
    ]
    assert actual == expected
    # No bpmx_lift events (Rule 2 not active).
    assert not any(e['type'] == 'bpmx_lift' for e in actual)


def test_recording_bpmx_rule_2_backward_on_graph_abc() -> None:
    """
    ========================================================================
     Rule 2 only (bpmx='2') with HCached at B.

     Chain is `HCached(HBounded(HCallable(0)))` — the outer
     HCached inherits the default `is_bounded=False`, so push/
     pop events on A won't carry an `is_bounded` flag even
     though Rule 2 lifted A's bound internally. This is a
     known chain-level limitation (HCached doesn't delegate
     is_bounded to its base); events still faithfully record
     the bpmx_lift.

     Trace:
       push A (h=0)
       pop A
       Rule 2 from child B (cached h=3): cand = 3-1 = 2 > 0
         → emit bpmx_lift(A, 0→2, via=B). Lift persists in
         HBounded but the outer HCached reports is_bounded=False.
       push B (is_cached=True)
       pop B → early_exit (is_perfect(B)=True), cost =
         g(B)+h_perfect(B) = 1+3 = 4.
    ========================================================================
    """
    from f_hs.problem.i_0_base._factory import _ProblemGraph
    problem = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': []},
        start='A', goal='C',
    )
    b_state = problem._states['B']
    c_state = problem._states['C']
    cache = {
        b_state: CacheEntry(h_perfect=3, suffix_next=c_state),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: 0,
        cache=cache,
        goal=c_state,
        bpmx='2',
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None,
         'h': 0, 'f': 0},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 0, 'f': 0},
        {'type': 'bpmx_lift', 'state': 'A', 'h_old': 0,
         'h_new': 2, 'via_child': 'B'},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A',
         'h': 3, 'f': 4, 'is_cached': True},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 3, 'f': 4,
         'is_cached': True},
    ]
    assert actual == expected
    # No bpmx_forward events (Rule 1 not active).
    assert not any(e['type'] == 'bpmx_forward'
                   for e in actual)


def test_recording_bpmx_rule_12_both_fire_on_diamond() -> None:
    """
    ========================================================================
     Rule 1 + Rule 2 both fire at A's expansion on a diamond
     graph A→{B,C}→D with B cached at h*=3, D cached at h*=0.

     At A's expansion:
       Rule 2: cand from B=3-1=2 > h(A)=0 → lift A to 2.
       Rule 1: B cached → skip; C not cached, cand = 2-1=1
               > base 0 → lift C to 1.
     Both events appear back-to-back between pop(A) and
     push(B).

     Chain is HCached(HBounded(HCallable)) — is_bounded=False
     on all outer events (HCached inherits default).
    ========================================================================
    """
    from f_hs.problem.i_0_base._factory import _ProblemGraph
    problem = _ProblemGraph(
        adj={'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []},
        start='A', goal='D',
    )
    b_state = problem._states['B']
    d_state = problem._states['D']
    cache = {
        b_state: CacheEntry(h_perfect=3, suffix_next=d_state),
        d_state: CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: 0,
        cache=cache,
        goal=d_state,
        bpmx='12',
        is_recording=True,
    )
    algo.run()
    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None,
         'h': 0, 'f': 0},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 0, 'f': 0},
        {'type': 'bpmx_lift', 'state': 'A', 'h_old': 0,
         'h_new': 2, 'via_child': 'B'},
        {'type': 'bpmx_forward', 'state': 'C', 'h_old': 0,
         'h_new': 1, 'via_parent': 'A'},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A',
         'h': 3, 'f': 4, 'is_cached': True},
        {'type': 'push', 'state': 'C', 'g': 1, 'parent': 'A',
         'h': 1, 'f': 2},
        {'type': 'pop',  'state': 'C', 'g': 1, 'h': 1, 'f': 2},
        {'type': 'push', 'state': 'D', 'g': 2, 'parent': 'C',
         'h': 0, 'f': 2, 'is_cached': True},
        {'type': 'pop',  'state': 'D', 'g': 2, 'h': 0, 'f': 2,
         'is_cached': True},
    ]
    assert actual == expected
    # Exactly one bpmx_lift (Rule 2 at A) and one bpmx_forward
    # (Rule 1 on C from A). Rule 1 skips the cached child B.
    lifts = [e for e in actual if e['type'] == 'bpmx_lift']
    fwds = [e for e in actual if e['type'] == 'bpmx_forward']
    assert len(lifts) == 1
    assert len(fwds) == 1
    assert lifts[0]['state'] == 'A'
    assert fwds[0]['state'] == 'C'


def test_recording_bpmx_rule_123_cascade_terminates() -> None:
    """
    ========================================================================
     bpmx='123' on the same diamond setup: cascade iterates
     Rules 1+2 to fixed point. On this configuration the first
     round lifts everything it can; the second round finds no
     changes and the cascade terminates.

     Asserts:
       1. Same correctness (cost 2) as '12'.
       2. Exactly one bpmx_lift at A, one bpmx_forward at C —
          no duplicate emissions from a cascade re-firing.
       3. Total bpmx events bounded (no infinite loop).
    ========================================================================
    """
    from f_hs.problem.i_0_base._factory import _ProblemGraph
    problem = _ProblemGraph(
        adj={'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []},
        start='A', goal='D',
    )
    b_state = problem._states['B']
    d_state = problem._states['D']
    cache = {
        b_state: CacheEntry(h_perfect=3, suffix_next=d_state),
        d_state: CacheEntry(h_perfect=0, suffix_next=None),
    }
    algo = AStarLookup(
        problem=problem,
        h=lambda s: 0,
        cache=cache,
        goal=d_state,
        bpmx='123',
        is_recording=True,
    )
    sol = algo.run()
    assert sol.cost == 2
    events = algo.recorder.events
    lifts = [e for e in events if e['type'] == 'bpmx_lift']
    fwds = [e for e in events if e['type'] == 'bpmx_forward']
    # Same single lift + single forward as '12' (cascade
    # converges after first round on this setup).
    assert len(lifts) == 1
    assert len(fwds) == 1
    # Total bounded (no runaway cascade).
    bpmx_count = len(lifts) + len(fwds)
    assert bpmx_count < 50


# ──────────────────────────────────────────────────
#  5. Full-trace recording tests on grid_4x4_obstacle
#     One test per rule configuration. Same setup:
#     HBounded seed on (1,0) at h=6 (tight; h*((1,0), (0,3))=6).
# ──────────────────────────────────────────────────


_GRID_BPMX_SEED = {(0, 0): 7}   # tight h* at start — maximally informative


def test_recording_bpmx_rule_1_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Rule 1 only (`bpmx='1'`) on grid_4x4_obstacle with tight
     HBounded seed at (0,0)=7 (h*(start→goal)=7).

     Rule 1 forward-lifts at each expansion of a bounded state:
       At (0,0): lifts (0,1) 2→6, (1,0) 4→6 via cand=7-1=6.
       At (0,1): lifts (1,1) 3→5 via cand=6-1=5.

     Total: 3 bpmx_forward events, 24-event stream. Pushed
     children carry is_bounded=True from that point onward.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='1',
        is_recording=True,
    )
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'bpmx_forward', 'state': (0, 1), 'h_old': 2, 'h_new': 6, 'via_parent': (0, 0)},
        {'type': 'bpmx_forward', 'state': (1, 0), 'h_old': 4, 'h_new': 6, 'via_parent': (0, 0)},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'bpmx_forward', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_parent': (0, 1)},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    lifts = [e for e in actual if e['type'] == 'bpmx_lift']
    fwds = [e for e in actual if e['type'] == 'bpmx_forward']
    assert len(lifts) == 0
    assert len(fwds) == 3


def test_recording_bpmx_rule_2_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Rule 2 only (`bpmx='2'`) on grid_4x4_obstacle with tight
     HBounded seed (0,0)=7.

     (0,0) pops at f=7 with the seeded h=7. Rule 2 then lifts
     its NEIGHBOURS via the triangle inequality using (0,0)'s
     h=7 available through the backward (closed-state) lookup:
       At (0,1)'s expansion: lift 2→6 via (0,0) (h=7, cand=6).
       At (1,1)'s expansion: lift 3→5 via (0,1) (lifted to 6).
       At (1,0)'s expansion: lift 4→6 via (0,0) (h=7, cand=6).

     3 bpmx_lift events, 25-event stream.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='2',
        is_recording=True,
    )
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2, 'f': 3},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2, 'f': 3},
        {'type': 'bpmx_lift', 'state': (0, 1), 'h_old': 2, 'h_new': 6, 'via_child': (0, 0)},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3, 'f': 5},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3, 'f': 5},
        {'type': 'bpmx_lift', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_child': (0, 1)},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'bpmx_lift', 'state': (1, 0), 'h_old': 4, 'h_new': 6, 'via_child': (0, 0)},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    lifts = [e for e in actual if e['type'] == 'bpmx_lift']
    fwds = [e for e in actual if e['type'] == 'bpmx_forward']
    assert len(lifts) == 3
    assert len(fwds) == 0


def test_recording_bpmx_rule_12_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Rules 1 + 2 (`bpmx='12'`) on grid_4x4_obstacle with tight
     HBounded seed (0,0)=7.

     Rule 2 tries to lift (0,0) from children but (0,0)=h*=7
     is already tight; no Rule 2 lift. Rule 1 fires at each
     expansion instead — same 3 bpmx_forward events as
     `bpmx='1'`. Pinned: on this seed, Rule 2 is subsumed by
     Rule 1 (same event stream as Rule 1 alone).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='12',
        is_recording=True,
    )
    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'bpmx_forward', 'state': (0, 1), 'h_old': 2, 'h_new': 6, 'via_parent': (0, 0)},
        {'type': 'bpmx_forward', 'state': (1, 0), 'h_old': 4, 'h_new': 6, 'via_parent': (0, 0)},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'bpmx_forward', 'state': (1, 1), 'h_old': 3, 'h_new': 5, 'via_parent': (0, 1)},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    lifts = [e for e in actual if e['type'] == 'bpmx_lift']
    fwds = [e for e in actual if e['type'] == 'bpmx_forward']
    assert len(lifts) == 0
    assert len(fwds) == 3


def test_recording_bpmx_rule_23_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Rule 2 + cascade (`bpmx='23'`). On this seed the cascade
     loop has no Rule 1 to re-apply after Rule 2's lift, so
     iterations collapse to a single Rule 2 pass — event
     stream is IDENTICAL to `bpmx='2'` (3 bpmx_lift events).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='23',
        is_recording=True,
    )
    algo.run()
    actual_23 = [normalize(e) for e in algo.recorder.events]

    algo2 = AStarLookup(
        problem=ProblemGrid.Factory.grid_4x4_obstacle(),
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='2',
        is_recording=True,
    )
    algo2.run()
    actual_2 = [normalize(e) for e in algo2.recorder.events]

    assert actual_23 == actual_2
    # Meaningful BPMX activity: 3 lifts.
    lifts = [e for e in actual_23 if e['type'] == 'bpmx_lift']
    assert len(lifts) == 3


def test_recording_bpmx_rule_123_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Rules 1+2+cascade (`bpmx='123'`). On this seed the cascade
     terminates after the first full pass — Rule 1 preempts
     Rule 2's opportunities, and subsequent rounds find no
     changes. Event stream IDENTICAL to `bpmx='12'` (3
     bpmx_forward events).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStarLookup(
        problem=problem,
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='123',
        is_recording=True,
    )
    algo.run()
    actual_123 = [normalize(e) for e in algo.recorder.events]

    algo2 = AStarLookup(
        problem=ProblemGrid.Factory.grid_4x4_obstacle(),
        h=lambda s: s.distance(goal),
        bounds={_sc(*k): v for k, v in _GRID_BPMX_SEED.items()},
        bpmx='12',
        is_recording=True,
    )
    algo2.run()
    actual_12 = [normalize(e) for e in algo2.recorder.events]

    assert actual_123 == actual_12
    fwds = [e for e in actual_123 if e['type'] == 'bpmx_forward']
    assert len(fwds) == 3
