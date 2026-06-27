from f_hs.algo.i_0_oospp.i_1_bfs import BFS
from f_hs.algo.i_1_omspp.i_1_kbfs import KBFS
from f_hs.problem.i_0_base._factory import _ProblemGraph


def _graph_abc_multigoal(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C with configurable goal list.
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


# ──────────────────────────────────────────────────
#  Lifecycle
# ──────────────────────────────────────────────────


def test_kbfs_single_goal_like_plain_bfs() -> None:
    """
    ========================================================================
     k=1 behaves like plain BFS. One sub-search, one on_goal
     event, no frontier transitions.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C'])
    algo = KBFS(problem=p, is_recording=True)
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2
    events = algo.recorder.events
    on_goals = [e for e in events if e['type'] == 'on_goal']
    assert len(on_goals) == 1
    assert on_goals[0]['reason'] == 'expanded'
    assert not any(e['type'] == 'update_frontier' for e in events)


def test_kbfs_two_goals_both_expanded() -> None:
    """
    ========================================================================
     goals=[B, C]: sub-search 1 finds B (depth 1); sub-search 2
     resumes and finds C (depth 2).
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KBFS(problem=p, is_recording=True)
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'B': 1, 'C': 2}


# ──────────────────────────────────────────────────
#  Discovery order
# ──────────────────────────────────────────────────


def test_kbfs_on_goal_in_discovery_order() -> None:
    """
    ========================================================================
     KBFS observes goals in their BFS-discovery order, not in
     `problem.goals` input order. With goals=[C, B] and B at
     depth 1 < C at depth 2, the on_goal events fire in order
     B, C — but each carries the original input `goal_index`
     (B at index 1, C at index 0).

     All `reason` values are `'expanded'` — KBFS never emits
     `'already_closed'` (single-pass design observes each goal
     exactly once at its pop).
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    algo = KBFS(problem=p, is_recording=True)
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'C': 2, 'B': 1}
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    # Discovery order: B (depth 1) → C (depth 2).
    assert [e['state'].key for e in on_goals] == ['B', 'C']
    # Original input indices preserved: B at idx 1, C at idx 0.
    assert [e['goal_index'] for e in on_goals] == [1, 0]
    # All goals 'expanded' — `already_closed` is unused.
    assert [e['reason'] for e in on_goals] == [
        'expanded', 'expanded']


# ──────────────────────────────────────────────────
#  Recording schema
# ──────────────────────────────────────────────────


def test_kbfs_no_transition_or_h_update_events() -> None:
    """
    ========================================================================
     KBFS runs a single inner BFS pass — no per-goal sub-
     search restarts, so no `update_frontier` boundary markers
     and no `update_heuristic` events ever fire.
    ========================================================================
    """
    p = _graph_diamond_multigoal(goals=['B', 'D'])
    algo = KBFS(problem=p, is_recording=True)
    algo.run()
    events = algo.recorder.events
    assert not any(e['type'] == 'update_frontier' for e in events)
    assert not any(e['type'] == 'update_heuristic' for e in events)


# ──────────────────────────────────────────────────
#  Counters
# ──────────────────────────────────────────────────


def test_kbfs_counters_h_zero_decrease_zero() -> None:
    """
    ========================================================================
     KBFS has no heuristic and no Φ aggregation — its counter
     scaffold contains only frontier ops + memory snapshots.
     Heuristic / Φ / stale-pop counters are absent (declared
     off the scaffold, not zero). `cnt_decrease` is 0
     (FIFO has no decrease op → synthesized); `cnt_push` is real.
    ========================================================================
    """
    algo = KBFS.Factory.graph_abc_two_goals()
    algo.run()
    c = algo.counters
    assert 'cnt_h_search' not in c
    assert 'cnt_h_update' not in c
    assert 'cnt_phi_search' not in c
    assert 'cnt_phi_update' not in c
    assert 'cnt_pop_stale' not in c
    assert c['cnt_decrease'] == 0
    assert c['cnt_push'] >= 1


def test_kbfs_elapsed_update_zero_by_construction() -> None:
    """
    ========================================================================
     Phase stays in SEARCH the whole time — `elapsed_update`
     is 0.0 by construction.
    ========================================================================
    """
    algo = KBFS.Factory.graph_abc_two_goals()
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update == 0.0


# ──────────────────────────────────────────────────
#  Cross-algo equivalence
# ──────────────────────────────────────────────────


def test_kbfs_costs_match_independent_bfs() -> None:
    """
    ========================================================================
     KBFS and independent BFS-per-goal produce identical
     optimal costs on uniform-weight graphs.
    ========================================================================
    """
    indep = {}
    for goal_key in ('B', 'C'):
        p = _graph_abc_multigoal(goals=[goal_key])
        indep[goal_key] = BFS(problem=p).run().cost
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KBFS(problem=p)
    by_key = {g.key: s.cost for g, s in algo.run().items()}
    assert by_key == indep


def test_kbfs_reconstruct_path() -> None:
    """
    ========================================================================
     reconstruct_path(goal) walks parents back to start for
     both `expanded` and `already_closed` goals.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    algo = KBFS(problem=p)
    algo.run()
    c_state = p._states['C']
    b_state = p._states['B']
    assert [s.key for s in algo.reconstruct_path(c_state)] == [
        'A', 'B', 'C']
    assert [s.key for s in algo.reconstruct_path(b_state)] == [
        'A', 'B']
