import pytest

from f_hs.algo.i_1_omspp.i_1_kxastar import KxAStarOMSPP
from f_hs.algo.i_1_omspp.mixins.extendable import (
    ExtendableOMSPP,
    is_extendable,
)
from f_hs.problem.i_0_base._factory import _ProblemGraph


def _line_graph(goals: list[str]) -> _ProblemGraph:
    """
    ========================================================================
     A -> B -> C -> D -> E -> F line graph with configurable
     goal list.
    ========================================================================
    """
    p = _ProblemGraph(
        adj={'A': ['B'], 'B': ['C'], 'C': ['D'],
             'D': ['E'], 'E': ['F'], 'F': []},
        start='A',
        goal=goals[0],
    )
    p._goals = [p._states[k] for k in goals]
    return p


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


_LINE_POS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}


# ──────────────────────────────────────────────────
#  1. Capability
# ──────────────────────────────────────────────────


def test_kxastar_is_extendable() -> None:
    """
    ========================================================================
     KxAStarOMSPP satisfies the ExtendableOMSPP protocol.
    ========================================================================
    """
    algo = KxAStarOMSPP.Factory.graph_abc_two_goals()
    assert isinstance(algo, ExtendableOMSPP)
    assert is_extendable(algo)
    assert callable(algo.extend)


# ──────────────────────────────────────────────────
#  2. Preconditions
# ──────────────────────────────────────────────────


def test_extend_before_run_raises() -> None:
    p = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    with pytest.raises(RuntimeError):
        algo.extend([p._states['D']])


def test_extend_empty_goals_raises() -> None:
    p = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    with pytest.raises(ValueError):
        algo.extend([])


# ──────────────────────────────────────────────────
#  3. Baseline parity
# ──────────────────────────────────────────────────


def test_extend_matches_single_shot() -> None:
    """
    ========================================================================
     run([B, C]) + extend([D, E]) yields the same per-goal
     costs as a single-shot run([B, C, D, E]).
    ========================================================================
    """
    p_full = _line_graph(goals=['B', 'C', 'D', 'E'])
    baseline = KxAStarOMSPP(problem=p_full, h=_pos_h(_LINE_POS))
    sol_full = baseline.run()
    base_costs = {g.key: s.cost for g, s in sol_full.items()}

    p_inc = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p_inc, h=_pos_h(_LINE_POS))
    algo.run()
    sol_ext = algo.extend(
        [p_inc._states['D'], p_inc._states['E']])
    ext_costs = {g.key: s.cost for g, s in sol_ext.items()}
    assert ext_costs == base_costs


# ──────────────────────────────────────────────────
#  4. Mixin efficiency for kxA* — already_reached
#     fast-path skips A* on re-submitted goals
# ──────────────────────────────────────────────────


def test_extend_skips_already_solved_goal() -> None:
    """
    ========================================================================
     extend() re-submitting an already-solved goal hits the
     already_reached fast-path: NO new A* runs. cnt_expanded
     is unchanged across the extend call.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_recording=True)
    algo.run()
    expanded_before = algo.counters['cnt_expanded']

    sol2 = algo.extend([p._states['B']])
    by_key = {g.key: s for g, s in sol2.items()}
    assert by_key['B'].cost == 1
    # Last on_goal is the fast-path event.
    on_goals = [e for e in algo.recorder.events
                if e['type'] == 'on_goal']
    assert on_goals[-1]['reason'] == 'already_reached'
    # Counter unchanged — no A* ran.
    assert algo.counters['cnt_expanded'] == expanded_before


# ──────────────────────────────────────────────────
#  5. Sequence chain
# ──────────────────────────────────────────────────


def test_extend_chain_three_calls() -> None:
    """
    ========================================================================
     run([B]) → extend([C]) → extend([D]) → extend([E]). The
     SolutionOMSPP after each call spans all goals so far.
    ========================================================================
    """
    p = _line_graph(goals=['B'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    algo.extend([p._states['C']])
    algo.extend([p._states['D']])
    final = algo.extend([p._states['E']])
    costs = {g.key: s.cost for g, s in final.items()}
    assert costs == {'B': 1, 'C': 2, 'D': 3, 'E': 4}


# ──────────────────────────────────────────────────
#  6. Counter accumulation
# ──────────────────────────────────────────────────


def test_extend_counters_cumulative() -> None:
    """
    ========================================================================
     Counters accumulate across run() and extend().
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS))
    algo.run()
    before = dict(algo.counters)
    algo.extend([p._states['D']])
    after = dict(algo.counters)
    for k in ('cnt_h_search', 'cnt_push', 'cnt_pop',
              'cnt_expanded', 'cnt_generated'):
        assert after[k] >= before[k]


# ──────────────────────────────────────────────────
#  7. _repush_last_reached_goal is structurally inert
# ──────────────────────────────────────────────────


def test_repush_is_inert() -> None:
    """
    ========================================================================
     kxA*'s _repush_last_reached_goal is a no-op (no shared
     frontier). The mixin contract still requires the method
     to exist and to clear bookkeeping cleanly.
    ========================================================================
    """
    p = _line_graph(goals=['B', 'C'])
    algo = KxAStarOMSPP(problem=p, h=_pos_h(_LINE_POS),
                   is_recording=True)
    algo.run()
    pushes_before = sum(1 for e in algo.recorder.events
                        if e['type'] == 'push')

    # Manually invoke _repush_last_reached_goal (what
    # extend() would do) and verify no push events are
    # emitted.
    algo._repush_last_reached_goal()
    pushes_after = sum(1 for e in algo.recorder.events
                       if e['type'] == 'push')
    assert pushes_after == pushes_before
    # Bookkeeping cleared.
    assert algo._last_reached_goal is None
    assert algo._last_algo is None


# ──────────────────────────────────────────────────
#  8. run_nested convenience
# ──────────────────────────────────────────────────


def test_run_nested_kxastar() -> None:
    """
    ========================================================================
     KxAStarOMSPP.run_nested([P1, P2, P3]) solves a prefix-extending
     sequence; only genuinely-new goals trigger A*.
    ========================================================================
    """
    p1 = _line_graph(goals=['B'])
    p2 = _line_graph(goals=['B', 'C'])
    p3 = _line_graph(goals=['B', 'C', 'D'])
    algo = KxAStarOMSPP.run_nested(
        problems=[p1, p2, p3], h=_pos_h(_LINE_POS))
    by_key = {g.key: s.cost
              for g, s in algo.solutions.items()}
    assert by_key == {'B': 1, 'C': 2, 'D': 3}
