from f_hs.algo.i_1_mospp.i_1_bfs_flip import BFSFlipMOSPP
from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


def _graph_abc_multistart(starts: list[str],
                          goal: str) -> _ProblemGraph:
    """
    ========================================================================
     Undirected A -- B -- C with configurable start list and
     a single goal. The undirected adjacency satisfies the
     BFSFlipMOSPP precondition (the delegation relies on symmetric
     `successors`).
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['A', 'C'], 'C': ['B']},
        start=starts[0], goal=goal,
    )
    p._starts = [p._states[k] for k in starts]
    p._goals = [p._states[goal]]
    return p


def _graph_diamond_multistart(starts: list[str]
                              ) -> _ProblemGraph:
    """
    ========================================================================
     Undirected A -- {B, C} -- D with configurable start
     list and goal D.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B', 'C'], 'B': ['A', 'D'],
             'C': ['A', 'D'], 'D': ['B', 'C']},
        start=starts[0], goal='D',
    )
    p._starts = [p._states[k] for k in starts]
    p._goals = [p._states['D']]
    return p


# ──────────────────────────────────────────────────
#  1. Lifecycle
# ──────────────────────────────────────────────────


def test_kbfs_mospp_single_start() -> None:
    """
    ========================================================================
     k=1 behaves like a plain backward BFS from the goal. One
     `on_start` event, no transitions.
    ========================================================================
    """
    p = _graph_abc_multistart(starts=['A'], goal='C')
    algo = BFSFlipMOSPP(problem=p, is_recording=True)
    sols = algo.run()
    assert len(sols) == 1
    assert next(iter(sols.values())).cost == 2
    events = algo.recorder.events
    on_starts = [e for e in events if e['type'] == 'on_start']
    assert len(on_starts) == 1
    assert on_starts[0]['reason'] == 'expanded'
    assert not any(e['type'] == 'update_frontier' for e in events)


def test_kbfs_mospp_two_starts_both_expanded() -> None:
    """
    ========================================================================
     starts=[A, B], goal=C: single backward BFS pass from C
     reaches B (depth 1) and A (depth 2). On-start events fire
     in discovery (depth) order — B first, then A.
    ========================================================================
    """
    p = _graph_abc_multistart(starts=['A', 'B'], goal='C')
    algo = BFSFlipMOSPP(problem=p, is_recording=True)
    sols = algo.run()
    by_key = {s.key: v.cost for s, v in sols.items()}
    assert by_key == {'A': 2, 'B': 1}
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    # Discovery (depth) order: B at depth 1, A at depth 2.
    assert [e['state'].key for e in on_starts] == ['B', 'A']
    # Input indices preserved: A=0, B=1.
    assert [e['start_index'] for e in on_starts] == [1, 0]
    assert [e['reason'] for e in on_starts] == [
        'expanded', 'expanded']


def test_kbfs_mospp_unreachable_start() -> None:
    """
    ========================================================================
     A start with no path to the goal returns cost=inf with
     reason='unreachable'.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['A'], 'X': []},
        start='A', goal='B',
    )
    p._starts = [p._states['A'], p._states['X']]
    p._goals = [p._states['B']]
    algo = BFSFlipMOSPP(problem=p, is_recording=True)
    sols = algo.run()
    assert sols[p._states['X']].cost == float('inf')
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    reasons = {e['state'].key: e['reason'] for e in on_starts}
    assert reasons == {'A': 'expanded', 'X': 'unreachable'}


# ──────────────────────────────────────────────────
#  2. Duplicate start
# ──────────────────────────────────────────────────


def test_kbfs_mospp_duplicate_start() -> None:
    """
    ========================================================================
     starts=[A, A]: single inner pass observes A once but emits
     one `on_start` per duplicate index.
    ========================================================================
    """
    algo = BFSFlipMOSPP.Factory.graph_abc_repeated_start()
    algo.recorder.is_active = True
    sols = algo.run()
    by_key = {s.key: v.cost for s, v in sols.items()}
    # State-keyed dict collapses duplicates to one entry.
    assert by_key == {'A': 1}
    on_starts = [e for e in algo.recorder.events
                 if e['type'] == 'on_start']
    # Both duplicate indices emit.
    assert [e['start_index'] for e in on_starts] == [0, 1]
    assert [e['reason'] for e in on_starts] == [
        'expanded', 'expanded']


# ──────────────────────────────────────────────────
#  3. Recording schema
# ──────────────────────────────────────────────────


def test_kbfs_mospp_no_transition_or_on_goal() -> None:
    """
    ========================================================================
     BFSFlipMOSPP delegates to OMSPP KBFS but the recorder shim
     rewrites `on_goal` → `on_start`. Stream must NOT contain
     `on_goal`, `update_frontier`, or `update_heuristic` events.
    ========================================================================
    """
    p = _graph_diamond_multistart(starts=['A', 'B'])
    algo = BFSFlipMOSPP(problem=p, is_recording=True)
    algo.run()
    events = algo.recorder.events
    assert not any(e['type'] == 'on_goal' for e in events)
    assert not any(e['type'] == 'update_frontier'
                   for e in events)
    assert not any(e['type'] == 'update_heuristic'
                   for e in events)


# ──────────────────────────────────────────────────
#  4. Counter scaffold
# ──────────────────────────────────────────────────


def test_kbfs_mospp_counter_scaffold() -> None:
    """
    ========================================================================
     BFSFlipMOSPP uses the base AlgoMOSPP scaffold unchanged —
     no heuristic, no Φ, so no `cnt_h_*` / `cnt_phi_*` /
     `cnt_pop_stale` counters on the scaffold. `cnt_decrease`
     is 0 (FIFO has no decrease op → synthesized at algo level).
    ========================================================================
    """
    algo = BFSFlipMOSPP.Factory.graph_abc_two_starts()
    algo.run()
    c = algo.counters
    assert 'cnt_h_search' not in c
    assert 'cnt_h_update' not in c
    assert 'cnt_phi_search' not in c
    assert 'cnt_phi_update' not in c
    assert 'cnt_pop_stale' not in c
    assert c['cnt_decrease'] == 0
    assert c['cnt_push'] >= 1


def test_kbfs_mospp_elapsed_update_is_zero() -> None:
    """
    ========================================================================
     BFSFlipMOSPP never enters PHASE_UPDATE — `elapsed_update` is
     0.0 by construction.
    ========================================================================
    """
    algo = BFSFlipMOSPP.Factory.graph_abc_two_starts()
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update == 0.0


# ──────────────────────────────────────────────────
#  5. Multi-goal rejection
# ──────────────────────────────────────────────────


def test_kbfs_mospp_rejects_multi_goal_problem() -> None:
    """
    ========================================================================
     BFSFlipMOSPP requires exactly one goal. A multi-goal problem
     raises ValueError at construction.
    ========================================================================
    """
    import pytest
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['A', 'C'], 'C': ['B']},
        start='A', goal='C',
    )
    p._starts = [p._states['A']]
    p._goals = [p._states['B'], p._states['C']]
    with pytest.raises(ValueError):
        BFSFlipMOSPP(problem=p)


# ──────────────────────────────────────────────────
#  6. Cross-algo equivalence
# ──────────────────────────────────────────────────


def test_kbfs_mospp_costs_match_kxastar() -> None:
    """
    ========================================================================
     BFSFlipMOSPP and AStarRepMOSPP must produce identical per-
     start optimal costs on the canonical MOSPP grid (the
     reference baseline). Uniform weights — KBFS is valid.
    ========================================================================
    """
    p1 = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    p2 = ProblemGrid.Factory.grid_4x4_obstacle_mospp()
    a = BFSFlipMOSPP(problem=p1)
    b = AStarRepMOSPP(
        problem=p2,
        h=lambda s, g: float(s.key.distance(g.key)),
    )
    a_costs = {(s.key.row, s.key.col): v.cost
               for s, v in a.run().items()}
    b_costs = {(s.key.row, s.key.col): v.cost
               for s, v in b.run().items()}
    assert a_costs == b_costs


# ──────────────────────────────────────────────────
#  7. Path reconstruction
# ──────────────────────────────────────────────────


def test_kbfs_mospp_reconstruct_path() -> None:
    """
    ========================================================================
     reconstruct_path(start) returns [start, ..., goal] —
     the MOSPP direction (reversed from the inner OMSPP).
    ========================================================================
    """
    p = _graph_abc_multistart(starts=['A', 'B'], goal='C')
    algo = BFSFlipMOSPP(problem=p)
    algo.run()
    a_state = p._states['A']
    b_state = p._states['B']
    assert [s.key for s in algo.reconstruct_path(a_state)] == [
        'A', 'B', 'C']
    assert [s.key for s in algo.reconstruct_path(b_state)] == [
        'B', 'C']
