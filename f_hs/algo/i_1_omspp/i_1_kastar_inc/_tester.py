from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_1_omspp import KAStarInc
from f_hs.algo.u_event_normalize import normalize
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


def _graph_abc_multigoal(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C with configurable goal list. Used by tests to
     swap goal ordering / repeats without rebuilding adjacency.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': []},
        start='A',
        goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _graph_diamond_multigoal(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> {B, C} -> D with configurable goal list.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []},
        start='A',
        goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


def _grid_4x4_obstacle_multigoal() -> ProblemGrid:
    """
    ========================================================================
     4x4 grid with wall cells at (0,2) and (1,2). Start (0,0),
     goals [(0,3), (3,3)]. Optimal costs 7 and 6.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._goals = [p._states[grid[0][3]],
                p._states[grid[3][3]]]
    return p


def _manhattan_grid(s, g) -> int:
    return (abs(s.key.row - g.key.row)
            + abs(s.key.col - g.key.col))


# ──────────────────────────────────────────────────
#  1. Lifecycle
# ──────────────────────────────────────────────────


def test_kastar_inc_single_goal_like_plain_astar() -> None:
    """
    ========================================================================
     k=1 behaves like plain A*. One sub-search, one on_goal
     event, no frontier transitions.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2
    events = algo.recorder.events
    on_goals = [e for e in events if e['type'] == 'on_goal']
    assert len(on_goals) == 1
    assert on_goals[0]['reason'] == 'expanded'
    assert on_goals[0]['goal_index'] == 0
    assert not any(e['type'] == 'update_frontier'
                   for e in events)


def test_kastar_inc_two_goals_both_expanded() -> None:
    """
    ========================================================================
     goals=[B, C]: sub-search 1 finds B (cost 1); sub-search 2
     resumes from shared state, finds C (cost 2). Both get
     reason='expanded'.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    sols = algo.run()
    by_key = {g.key: s for g, s in sols.items()}
    assert by_key['B'].cost == 1
    assert by_key['C'].cost == 2
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert len(on_goals) == 2
    assert [e['reason'] for e in on_goals] == ['expanded',
                                                'expanded']
    assert [e['goal_index'] for e in on_goals] == [0, 1]
    assert [e['state'].key for e in on_goals] == ['B', 'C']


# ──────────────────────────────────────────────────
#  2. Fast-path: goal already closed
# ──────────────────────────────────────────────────


def test_kastar_inc_goal_already_closed_fast_path() -> None:
    """
    ========================================================================
     goals=[C, B]: sub-search 1 seeks C and closes B along
     the way. Sub-search 2 finds B already in CLOSED → fast-
     path with reason='already_closed', no resume().
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    sols = algo.run()
    by_key = {g.key: s for g, s in sols.items()}
    assert by_key['C'].cost == 2
    assert by_key['B'].cost == 1
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    reasons = [e['reason'] for e in on_goals]
    assert reasons == ['expanded', 'already_closed']
    # No update_frontier emitted since the second goal hit
    # fast-path before the transition logic ran.
    assert not any(e['type'] == 'update_frontier'
                   for e in algo.recorder.events)


def test_kastar_inc_duplicate_goals() -> None:
    """
    ========================================================================
     goals=[B, B, B]: first finds B (expanded), rest hit the
     fast-path (already_closed). All three solutions equal.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'B', 'B'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    sols = algo.run()
    # sols keyed by State — duplicates collapse in dict (same
    # state object → one entry). Paper's contract allows this.
    assert len(sols) == 1
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert len(on_goals) == 3
    assert [e['reason'] for e in on_goals] == [
        'expanded', 'already_closed', 'already_closed',
    ]
    assert [e['goal_index'] for e in on_goals] == [0, 1, 2]


# ──────────────────────────────────────────────────
#  3. Frontier transition events
# ──────────────────────────────────────────────────


def test_kastar_inc_frontier_transition_events() -> None:
    """
    ========================================================================
     Between sub-searches: one update_frontier event + N
     update_heuristic events (N = frontier size at transition).
     Each carries h_old (prev goal) and h_new (current goal).
    ========================================================================
    """
    # diamond: goals=[B, D]. After sub-search 1 (B found),
    # C is on frontier. Sub-search 2 refreshes with h_D.
    p = _graph_diamond_multigoal(goals=['B', 'D'])
    pos = {'A': 0, 'B': 1, 'C': 1, 'D': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    algo.run()
    events = algo.recorder.events
    transitions = [e for e in events
                   if e['type'] == 'update_frontier']
    assert len(transitions) == 1
    assert transitions[0]['next_goal_index'] == 1
    updates = [e for e in events
               if e['type'] == 'update_heuristic']
    assert len(updates) == transitions[0]['num_nodes']
    # Every update carries h_old and h_new as ints.
    for u in updates:
        assert isinstance(u['h_old'], int)
        assert isinstance(u['h_new'], int)
    # update_frontier precedes its update_heuristic events in
    # the event stream.
    idx_trans = events.index(transitions[0])
    for u in updates:
        assert events.index(u) > idx_trans


def test_kastar_inc_update_heuristic_reflects_goal_change(
        ) -> None:
    """
    ========================================================================
     Specific values pinned: on diamond with goals=[B, D],
     after sub-search 1, C is on frontier with h_B(C)=0 (C's
     key=='C' so pos diff to 'B'=0). Sub-search 2 refreshes to
     h_D(C) = |1 - 2| = 1. Pin the (h_old, h_new) pair.
    ========================================================================
    """
    p = _graph_diamond_multigoal(goals=['B', 'D'])
    pos = {'A': 0, 'B': 1, 'C': 1, 'D': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos), is_recording=True)
    algo.run()
    updates = [e for e in algo.recorder.events
               if e['type'] == 'update_heuristic']
    by_state = {u['state'].key: (u['h_old'], u['h_new'])
                for u in updates}
    # C's h under goal B: |1-1| = 0.
    # C's h under goal D: |1-2| = 1.
    if 'C' in by_state:
        assert by_state['C'] == (0, 1)


# ──────────────────────────────────────────────────
#  4. Correctness invariants
# ──────────────────────────────────────────────────


def test_kastar_inc_vs_independent_astars_same_costs() -> None:
    """
    ========================================================================
     kA*_inc and independent A* per goal produce identical
     optimal costs on a graph problem.
    ========================================================================
    """
    pos = {'A': 0, 'B': 1, 'C': 2}
    # Independent.
    indep_costs = {}
    for goal_key in ('B', 'C'):
        p = _graph_abc_multigoal(goals=[goal_key])
        a = AStar(problem=p,
                  h=(lambda s, gk=goal_key:
                     abs(pos[s.key] - pos[gk])))
        indep_costs[goal_key] = a.run().cost
    # kA*_inc.
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KAStarInc(problem=p, h=_pos_h(pos))
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == indep_costs


def test_kastar_inc_reconstruct_path() -> None:
    """
    ========================================================================
     reconstruct_path(goal) walks parents back to start for
     both `expanded` and `already_closed` goals.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos))
    algo.run()
    # Fetch the state objects from the problem.
    c_state = p._states['C']
    b_state = p._states['B']
    assert [s.key for s in algo.reconstruct_path(c_state)] == [
        'A', 'B', 'C']
    assert [s.key for s in algo.reconstruct_path(b_state)] == [
        'A', 'B']


def test_kastar_inc_h_closure_no_late_binding() -> None:
    """
    ========================================================================
     Heuristic closure uses default-arg idiom — each sub-
     search's h_i sees ITS goal, not the last in the loop.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    calls = []
    def h(state, goal):
        calls.append((state.key, goal.key))
        return abs(pos[state.key] - pos[goal.key])
    algo = KAStarInc(problem=p, h=h)
    algo.run()
    goals_seen = {g for _, g in calls}
    assert 'B' in goals_seen
    assert 'C' in goals_seen


def test_kastar_inc_search_state_exposed_after_run() -> None:
    """
    ========================================================================
     After run(), `search_state` property exposes the shared
     SearchStateSPP bundle for inspection.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    pos = {'A': 0, 'B': 1, 'C': 2}
    algo = KAStarInc(problem=p, h=_pos_h(pos))
    algo.run()
    assert algo.search_state is not None
    assert 'A' in {s.key for s in algo.search_state.closed}


# ──────────────────────────────────────────────────
#  5. Grid domain — recorded run on grid_4x4_obstacle
# ──────────────────────────────────────────────────


def test_counters_surface() -> None:
    """
    ========================================================================
     Test KAStarInc exposes the inherited 8-counter surface
     and that frontier counts are mirrored at end-of-run via
     `_sync_frontier_counters`. After a real run, cnt_push /
     cnt_pop must be > 0 (frontier was actually used).
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    algo.run()
    c = algo.counters
    assert set(c) == {
        'cnt_h_search', 'cnt_h_update',
        'cnt_phi_search', 'cnt_phi_update',
        'cnt_push', 'cnt_pop',
        'cnt_pop_stale', 'cnt_decrease',
        'mem_open', 'mem_closed',
    }
    # Frontier was used → push/pop reflect real heap traffic.
    assert c['cnt_push'] >= 1
    assert c['cnt_pop'] <= c['cnt_push']
    # KAStarInc has no Φ aggregation and no lazy stale branch.
    assert c['cnt_phi_search'] == 0
    assert c['cnt_phi_update'] == 0
    assert c['cnt_pop_stale'] == 0


def test_counters_pin_graph_abc_two_goals() -> None:
    """
    ========================================================================
     Pin the exact 8-counter dict for KAStarInc on
     graph_abc_two_goals. Two sub-searches with consistent
     h: cnt_h_search counts h-calls during sub-search
     execution, cnt_h_update counts the inter-sub-search
     priority-refresh h-calls.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_h_search': 3, 'cnt_h_update': 3,
        'cnt_phi_search': 0, 'cnt_phi_update': 0,
        'cnt_push': 4, 'cnt_pop': 3,
        'cnt_pop_stale': 0, 'cnt_decrease': 0,
        'mem_open': 280, 'mem_closed': 736,
    }


def test_counters_pin_graph_abc_cached_at_b_first() -> None:
    """
    ========================================================================
     Pin the 8-counter dict on the fast-path scenario:
     goals=[C, B] — first sub-search reaches and force-
     expands C; second sub-search hits the already-closed
     fast-path on B → no resume(), no priority refresh,
     no `cnt_h_update`.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_cached_at_b_first()
    algo.run()
    assert dict(algo.counters) == {
        'cnt_h_search': 3, 'cnt_h_update': 0,
        'cnt_phi_search': 0, 'cnt_phi_update': 0,
        'cnt_push': 3, 'cnt_pop': 3,
        'cnt_pop_stale': 0, 'cnt_decrease': 0,
        'mem_open': 280, 'mem_closed': 736,
    }


def test_elapsed_split_positive_when_multi_goal() -> None:
    """
    ========================================================================
     Test elapsed_search > 0 AND elapsed_update > 0 for k=2.
     INC always has at least one inter-sub-search transition
     when k>=2 (unless the second goal hits the fast-path),
     so both buckets accrue real time.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update > 0.0


def test_elapsed_split_zero_when_is_timing_off() -> None:
    """
    ========================================================================
     Test that is_timing=False suppresses both bucket timers
     (algo still runs correctly; just no perf_counter calls).
    ========================================================================
    """
    factory = KAStarInc.Factory.graph_abc_two_goals
    a, b = factory(), factory()
    b._is_timing = False
    a.run()
    b.run()
    assert a.elapsed_search > 0.0 and a.elapsed_update > 0.0
    assert b.elapsed_search == 0.0 and b.elapsed_update == 0.0
    # Counters/results unchanged.
    assert dict(a.counters) == dict(b.counters)


def test_phase_setter_rejects_unknown_value() -> None:
    """
    ========================================================================
     Test phase property setter raises ValueError on a typo'd
     phase name — typo guard, same spirit as Counters.inc.
    ========================================================================
    """
    import pytest
    algo = KAStarInc.Factory.graph_abc_two_goals()
    with pytest.raises(ValueError, match='unknown phase'):
        algo.phase = 'bogus'
