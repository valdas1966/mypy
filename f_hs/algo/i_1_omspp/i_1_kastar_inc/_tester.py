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
     fast-path via `self._solutions` (already_reached). Under
     the lazy re-push design, B is on OPEN — not in
     shared.closed — so the predicate routes through
     `self._solutions`, not `shared.closed`.
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
        'expanded', 'already_reached', 'already_reached',
    ]
    assert [e['goal_index'] for e in on_goals] == [0, 1, 2]


# ──────────────────────────────────────────────────
#  3. Frontier transition events
# ──────────────────────────────────────────────────


def test_kastar_inc_frontier_transition_event() -> None:
    """
    ========================================================================
     Between sub-searches: exactly one `update_frontier`
     boundary event per transition, carrying `num_nodes` (the
     frontier size at the moment of refresh) and
     `next_goal_index`. The per-state `update_heuristic`
     cluster was removed — heuristic re-keying happens via
     `refresh_priorities()` and is observable through
     `cnt_h_update` and the silent re-push activity.
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
    assert isinstance(transitions[0]['num_nodes'], int)
    assert transitions[0]['num_nodes'] >= 1
    # `update_heuristic` is NOT emitted (removed by design).
    assert not any(e['type'] == 'update_heuristic'
                   for e in events)


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
     Test KAStarInc exposes its declared counter surface
     (heuristic + frontier + memory) and that frontier counts
     are mirrored at end-of-run via `_sync_frontier_counters`.
     Φ counters and `cnt_pop_stale` are ABSENT — KAStarInc has
     no aggregation and no lazy stale-pop branch, so they're
     declared off the scaffold (not zero). After a real run,
     cnt_push / cnt_pop must be > 0 (frontier was used).
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    algo.run()
    c = algo.counters
    assert set(c) == {
        'cnt_h_search', 'cnt_h_update',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
        'mem_open', 'mem_closed', 'mem_total',
    }
    # Frontier was used → push/pop reflect real heap traffic.
    assert c['cnt_push'] >= 1
    assert c['cnt_pop'] <= c['cnt_push']
    # Off-scaffold counters confirmed absent.
    assert 'cnt_phi_search' not in c
    assert 'cnt_phi_update' not in c
    assert 'cnt_pop_stale' not in c


def test_counters_pin_graph_abc_two_goals() -> None:
    """
    ========================================================================
     Pin the counter dict for KAStarInc on
     graph_abc_two_goals (goals=[B, C]). Lazy re-push:
     after sub-search 0 reaches B, B re-enters OPEN via
     `_lazy_repush` (+1 cnt_push, NO cnt_h_search — the
     provably-zero h_i(B, B) is skipped); the transition
     refreshes a 1-state frontier (+1 cnt_push silent,
     +3 cnt_h_update); sub-search 1 pops B, expands → push
     C, pops C (last goal, no re-push).
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_two_goals()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 3, 'cnt_h_update': 1,
        'cnt_push': 5, 'cnt_pop': 4, 'cnt_decrease': 0,
        'cnt_expanded': 2, 'cnt_generated': 3,
    }


def test_counters_pin_graph_abc_cached_at_b_first() -> None:
    """
    ========================================================================
     Pin the counter dict on the fast-path scenario:
     goals=[C, B] — sub-search 0 reaches C and re-pushes it
     via `_lazy_repush` (h-free; no cnt_h_search added);
     sub-search 1 hits the already-closed fast-path on B (B
     was popped+expanded as collateral by sub-search 0). No
     resume(), no priority refresh, no `cnt_h_update`.
    ========================================================================
    """
    algo = KAStarInc.Factory.graph_abc_cached_at_b_first()
    algo.run()
    counters = {k: v for k, v in algo.counters.items()
                if not k.startswith('mem_')}
    assert counters == {
        'cnt_h_search': 3, 'cnt_h_update': 0,
        'cnt_push': 4, 'cnt_pop': 3, 'cnt_decrease': 0,
        'cnt_expanded': 2, 'cnt_generated': 3,
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
