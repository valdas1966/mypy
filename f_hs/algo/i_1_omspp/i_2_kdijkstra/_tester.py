from f_hs.algo.i_0_oospp.i_2_dijkstra import Dijkstra
from f_hs.algo.i_1_omspp.i_2_kdijkstra import KDijkstra
from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
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


def test_kdijkstra_single_goal_like_plain_dijkstra() -> None:
    """
    ========================================================================
     k=1 behaves like plain Dijkstra. One sub-search, one
     on_goal event, no frontier transitions.
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C'])
    algo = KDijkstra(problem=p, is_recording=True)
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2
    events = algo.recorder.events
    on_goals = [e for e in events if e['type'] == 'on_goal']
    assert len(on_goals) == 1
    assert on_goals[0]['reason'] == 'expanded'
    assert not any(e['type'] == 'update_frontier' for e in events)


def test_kdijkstra_two_goals_both_expanded() -> None:
    """
    ========================================================================
     goals=[B, C]: sub-search 1 finds B (cost 1); sub-search 2
     resumes and finds C (cost 2).
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KDijkstra(problem=p, is_recording=True)
    sols = algo.run()
    by_key = {g.key: s for g, s in sols.items()}
    assert by_key['B'].cost == 1
    assert by_key['C'].cost == 2


# ──────────────────────────────────────────────────
#  Fast-path
# ──────────────────────────────────────────────────


def test_kdijkstra_on_goal_in_discovery_order() -> None:
    """
    ========================================================================
     KDijkstra observes goals in their g-order, not in
     `problem.goals` input order. With goals=[C, B] and B at
     g=1 < C at g=2, the on_goal events fire in order B, C
     — but each carries the original input `goal_index`
     (B at index 1, C at index 0).

     All `reason` values are `'expanded'` — KDijkstra never
     emits `'already_closed'` (single-pass design observes
     each goal exactly once at its pop).
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C', 'B'])
    algo = KDijkstra(problem=p, is_recording=True)
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'C': 2, 'B': 1}
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert [e['state'].key for e in on_goals] == ['B', 'C']
    assert [e['goal_index'] for e in on_goals] == [1, 0]
    assert [e['reason'] for e in on_goals] == [
        'expanded', 'expanded']


# ──────────────────────────────────────────────────
#  Recording schema
# ──────────────────────────────────────────────────


def test_kdijkstra_no_transition_or_h_update_events() -> None:
    """
    ========================================================================
     KDijkstra runs a single inner Dijkstra pass — no per-
     goal sub-search restarts, so no `update_frontier`
     boundary markers and no `update_heuristic` events ever
     fire.
    ========================================================================
    """
    p = _graph_diamond_multigoal(goals=['B', 'D'])
    algo = KDijkstra(problem=p, is_recording=True)
    algo.run()
    events = algo.recorder.events
    assert not any(e['type'] == 'update_frontier' for e in events)
    assert not any(e['type'] == 'update_heuristic' for e in events)


def test_kdijkstra_inner_sub_algo_is_dijkstra() -> None:
    """
    ========================================================================
     KDijkstra wraps `Dijkstra` (not plain AStar) for the
     inner search — verifies via the type of the constructed
     inner instance after `run()`. Cleaner event schema
     (`Dijkstra._enrich_event` drops h and f, since both are
     constant or derivable).
    ========================================================================
    """
    p = _graph_abc_multigoal(goals=['C'])
    algo = KDijkstra(problem=p)
    algo.run()
    # Walk the MRO of the inner instance — `Dijkstra` should
    # appear in it (the inner is a `_MultiGoalDijkstra` which
    # inherits from `Dijkstra`).
    assert isinstance(algo._inner, Dijkstra)


# ──────────────────────────────────────────────────
#  Counters
# ──────────────────────────────────────────────────


def test_kdijkstra_counters_h_zero() -> None:
    """
    ========================================================================
     KDijkstra has no heuristic and no Φ aggregation — its
     counter scaffold contains only frontier ops + memory
     snapshots. Heuristic / Φ / stale-pop counters are absent
     (declared off the scaffold, not zero). Frontier counters
     are real.
    ========================================================================
    """
    algo = KDijkstra.Factory.graph_abc_two_goals()
    algo.run()
    c = algo.counters
    assert 'cnt_h_search' not in c
    assert 'cnt_h_update' not in c
    assert 'cnt_phi_search' not in c
    assert 'cnt_phi_update' not in c
    assert 'cnt_pop_stale' not in c
    assert c['cnt_push'] >= 1


def test_kdijkstra_elapsed_update_zero_by_construction() -> None:
    """
    ========================================================================
     Phase stays in SEARCH the whole time — `elapsed_update`
     is 0.0 by construction (matches AGG-lazy's structurally-
     zero pattern).
    ========================================================================
    """
    algo = KDijkstra.Factory.graph_abc_two_goals()
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update == 0.0


# ──────────────────────────────────────────────────
#  Cross-algo equivalence
# ──────────────────────────────────────────────────


def test_kdijkstra_costs_match_independent_dijkstras() -> None:
    """
    ========================================================================
     KDijkstra and independent Dijkstra-per-goal produce
     identical optimal costs. Sanity check on optimality.
    ========================================================================
    """
    indep = {}
    for goal_key in ('B', 'C'):
        p = _graph_abc_multigoal(goals=[goal_key])
        indep[goal_key] = Dijkstra(problem=p).run().cost
    p = _graph_abc_multigoal(goals=['B', 'C'])
    algo = KDijkstra(problem=p)
    by_key = {g.key: s.cost for g, s in algo.run().items()}
    assert by_key == indep


def test_kdijkstra_costs_match_kastar_inc_with_zero_h() -> None:
    """
    ========================================================================
     KDijkstra is `KAStarInc(h≡0)` semantically. Both must
     return identical optimal costs on the same problem.
    ========================================================================
    """
    p = _graph_diamond_multigoal(goals=['B', 'D'])
    a = KAStarInc(problem=p, h=lambda s, g: 0)
    b = KDijkstra(problem=p)
    a_costs = {g.key: s.cost for g, s in a.run().items()}
    b_costs = {g.key: s.cost for g, s in b.run().items()}
    assert a_costs == b_costs
