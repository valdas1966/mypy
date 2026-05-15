import pytest

from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
from f_hs.problem.i_0_base._factory import _ProblemGraph


def _abc(goals: list[str]) -> _ProblemGraph:
    p = _ProblemGraph(adj={'A': ['B'], 'B': ['C'], 'C': []},
                      start='A', goal=goals[0])
    p._goals = [p._states[k] for k in goals]
    return p


def _diamond(goals: list[str]) -> _ProblemGraph:
    p = _ProblemGraph(
        adj={'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []},
        start='A', goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


# ──────────────────────────────────────────────────
#  1. Validation
# ──────────────────────────────────────────────────


def test_agg_rejects_invalid_string() -> None:
    """
    ========================================================================
     Unknown agg string raises ValueError.
    ========================================================================
    """
    with pytest.raises(ValueError, match='agg must be one of'):
        KAStarAgg(problem=_abc(['B']),
                  h=_pos_h({'A': 0, 'B': 1, 'C': 2}),
                  agg='BOGUS')


def test_agg_accepts_custom_callable() -> None:
    """
    ========================================================================
     Custom Callable accepted; display name 'CUSTOM'.
    ========================================================================
    """
    def my_agg(hs):
        return max(hs) - min(hs) if hs else 0
    algo = KAStarAgg(
        problem=_abc(['B']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 2}),
        agg=my_agg,
    )
    assert algo.agg == 'CUSTOM'


# ──────────────────────────────────────────────────
#  2. Each aggregation produces a valid run
# ──────────────────────────────────────────────────


@pytest.mark.parametrize('agg', ['MIN', 'MAX', 'AVG', 'RND', 'PROJECTION'])
def test_agg_all_five_terminate_on_diamond(agg: str) -> None:
    """
    ========================================================================
     All 5 aggregations terminate and return a solution per
     goal (cost may differ for non-admissible Φ like MAX).
    ========================================================================
    """
    import random
    random.seed(0)   # deterministic RND for this test
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg=agg,
    )
    sols = algo.run()
    assert len(sols) == 2
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key['B'] == 1   # A -> B costs 1
    assert by_key['D'] == 2   # A -> B -> D or A -> C -> D costs 2


# ──────────────────────────────────────────────────
#  3. Consistency across storage modes
# ──────────────────────────────────────────────────


@pytest.mark.parametrize('store_vector', [True, False])
def test_agg_vector_and_aggregate_storage_equivalent(
        store_vector: bool) -> None:
    """
    ========================================================================
     store_vector=True and store_vector=False produce the same
     optimal costs (MIN is deterministic).
    ========================================================================
    """
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg='MIN',
        store_vector=store_vector,
    )
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'B': 1, 'D': 2}


# ──────────────────────────────────────────────────
#  4. Lazy vs Eager equivalence (with antitone MIN)
# ──────────────────────────────────────────────────


@pytest.mark.parametrize('is_lazy', [True, False])
def test_agg_lazy_and_eager_same_costs(is_lazy: bool) -> None:
    """
    ========================================================================
     is_lazy=True and is_lazy=False return the same costs on
     admissible MIN aggregation.
    ========================================================================
    """
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg='MIN',
        is_lazy=is_lazy,
    )
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == {'B': 1, 'D': 2}


# ──────────────────────────────────────────────────
#  5. Cost equivalence with independent A*
# ──────────────────────────────────────────────────


def test_agg_min_matches_independent_astars() -> None:
    """
    ========================================================================
     kA*_agg with MIN (admissible Φ on consistent h) returns
     the same optimal costs as running independent A* per goal.
    ========================================================================
    """
    pos = {'A': 0, 'B': 1, 'C': 1, 'D': 2}
    # Independent.
    indep = {}
    for gk in ('B', 'D'):
        p = _diamond([gk])
        a = AStar(problem=p,
                  h=lambda s, gk=gk: abs(pos[s.key] - pos[gk]))
        indep[gk] = a.run().cost
    # kA*_agg MIN.
    p = _diamond(['B', 'D'])
    algo = KAStarAgg(problem=p, h=_pos_h(pos), agg='MIN')
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key == indep


# ──────────────────────────────────────────────────
#  6. Unreachable goal
# ──────────────────────────────────────────────────


def test_agg_unreachable_goal_returns_inf() -> None:
    """
    ========================================================================
     A goal with no path returns SolutionSPP(cost=inf); on_goal
     emitted with reason='unreachable'.
    ========================================================================
    """
    # Graph A -> B. Start = A. Goals = [B, X] where X is isolated.
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': [], 'X': []},
        start='A', goal='B',
    )
    p._goals = [p._states['B'], p._states['X']]
    algo = KAStarAgg(
        problem=p,
        h=lambda s, g: 0,   # trivial zero-heuristic
        agg='MIN',
        is_recording=True,
    )
    sols = algo.run()
    by_key = {g.key: s.cost for g, s in sols.items()}
    assert by_key['B'] == 1
    assert by_key['X'] == float('inf')
    reasons = [e['reason'] for e in algo.recorder.events
               if e['type'] == 'on_goal']
    assert 'expanded' in reasons
    assert 'unreachable' in reasons


# ──────────────────────────────────────────────────
#  7. Event emission
# ──────────────────────────────────────────────────


def test_agg_emits_on_goal_per_goal() -> None:
    """
    ========================================================================
     One on_goal event per goal with correct goal_index.
    ========================================================================
    """
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg='MIN',
        is_recording=True,
    )
    algo.run()
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert len(on_goals) == 2
    assert sorted(e['goal_index'] for e in on_goals) == [0, 1]


def test_agg_eager_emits_update_frontier_between_goals() -> None:
    """
    ========================================================================
     With is_lazy=False, a found goal that leaves OPEN non-empty
     triggers an `update_frontier` boundary marker before the
     bulk refresh. Refresh re-pushes are silent (no events).
    ========================================================================
    """
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg='MIN',
        is_lazy=False,
        is_recording=True,
    )
    algo.run()
    transitions = [e for e in algo.recorder.events
                   if e['type'] == 'update_frontier']
    assert len(transitions) >= 1
    for t in transitions:
        assert t['num_nodes'] >= 0


def test_agg_lazy_emits_no_update_frontier() -> None:
    """
    ========================================================================
     With is_lazy=True, no `update_frontier` markers are
     emitted — refresh is inline at pop time and structurally
     belongs to search (no between-phase moment).
    ========================================================================
    """
    algo = KAStarAgg(
        problem=_diamond(['B', 'D']),
        h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
        agg='MIN',
        is_lazy=True,
        is_recording=True,
    )
    algo.run()
    assert not any(e['type'] == 'update_frontier'
                   for e in algo.recorder.events)


# ──────────────────────────────────────────────────
#  8. Path reconstruction
# ──────────────────────────────────────────────────


def test_agg_reconstruct_path() -> None:
    """
    ========================================================================
     reconstruct_path(goal) walks parents back to start for
     each reached goal.
    ========================================================================
    """
    p = _abc(['B', 'C'])
    algo = KAStarAgg(
        problem=p,
        h=_pos_h({'A': 0, 'B': 1, 'C': 2}),
        agg='MIN',
    )
    algo.run()
    b = p._states['B']
    c = p._states['C']
    assert [s.key for s in algo.reconstruct_path(b)] == ['A', 'B']
    assert [s.key for s in algo.reconstruct_path(c)] == ['A', 'B', 'C']


# ──────────────────────────────────────────────────
#  9. Grid domain — full per-config recording tests
#     live in `_tester_recording.py` (8 tests, one per
#     is_lazy × is_opt × store_vector cell).
# ──────────────────────────────────────────────────


def test_counters_surface() -> None:
    """
    ========================================================================
     Test KAStarAgg exposes the inherited 8-counter surface.
     Per-config exact-value pinning lives in
     `_tester_recording.py` (9 tests across the
     is_lazy × is_opt × store_vector × MIN/MAX matrix).
    ========================================================================
    """
    p = _abc(goals=['B', 'C'])
    h = _pos_h({'A': 2, 'B': 1, 'C': 0})
    algo = KAStarAgg(problem=p, h=h, agg='MIN')
    algo.run()
    c = algo.counters
    assert set(c) == {
        'cnt_h_search', 'cnt_h_update',
        'cnt_phi_search', 'cnt_phi_update',
        'cnt_push', 'cnt_pop', 'cnt_decrease',
        'cnt_expanded', 'cnt_generated',
        'mem_open', 'mem_closed', 'mem_aux',
    }
    assert c['cnt_pop'] <= c['cnt_push']
    assert c['cnt_pop'] >= 1
    assert c['cnt_phi_search'] >= 1   # at least one F computation
    assert c['mem_aux'] > 0   # _F_stored is always populated


def _make_2goal_agg(*, is_lazy: bool, is_opt: bool,
                    store_vector: bool) -> KAStarAgg:
    """
    ========================================================================
     Helper: build a 2-goal Agg on grid_4x4_obstacle for the
     elapsed-split tests across the 8 configs.
    ========================================================================
    """
    from f_hs.problem.i_1_grid import ProblemGrid
    p = ProblemGrid.Factory.grid_4x4_obstacle()
    grid = p.grid
    p._goals = [p._states[grid[0][3]], p._states[grid[3][3]]]

    def manhattan(s, g):
        return (abs(s.key.row - g.key.row)
                + abs(s.key.col - g.key.col))

    return KAStarAgg(problem=p, h=manhattan, agg='MIN',
                     is_lazy=is_lazy, is_opt=is_opt,
                     store_vector=store_vector)


@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_elapsed_split_eager_has_positive_update(
        is_opt: bool, store_vector: bool) -> None:
    """
    ========================================================================
     Eager Agg has between-phase _refresh_priorities → both
     elapsed_search and elapsed_update strictly positive.
     Verified across all 4 (is_opt × store_vector) sub-configs.
    ========================================================================
    """
    algo = _make_2goal_agg(is_lazy=False, is_opt=is_opt,
                           store_vector=store_vector)
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update > 0.0


@pytest.mark.parametrize('is_opt', [False, True])
@pytest.mark.parametrize('store_vector', [False, True])
def test_elapsed_split_lazy_has_zero_update(
        is_opt: bool, store_vector: bool) -> None:
    """
    ========================================================================
     Lazy Agg has NO between-phase moment by construction —
     refresh work happens inline at pop-time and is structurally
     part of search. So elapsed_update is exactly 0.0 for all
     4 lazy configs.
    ========================================================================
    """
    algo = _make_2goal_agg(is_lazy=True, is_opt=is_opt,
                           store_vector=store_vector)
    algo.run()
    assert algo.elapsed_search > 0.0
    assert algo.elapsed_update == 0.0


def test_elapsed_split_zero_when_is_timing_off() -> None:
    """
    ========================================================================
     Test is_timing=False suppresses both bucket timers across
     all 8 configs. Spot-check eager+opt+vec; the property
     setter branch is identical for all configs.
    ========================================================================
    """
    a = _make_2goal_agg(is_lazy=False, is_opt=True,
                        store_vector=True)
    b = _make_2goal_agg(is_lazy=False, is_opt=True,
                        store_vector=True)
    b._is_timing = False
    a.run()
    b.run()
    assert a.elapsed_search > 0.0 and a.elapsed_update > 0.0
    assert b.elapsed_search == 0.0 and b.elapsed_update == 0.0
    assert dict(a.counters) == dict(b.counters)
