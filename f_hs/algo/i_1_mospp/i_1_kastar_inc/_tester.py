"""
============================================================================
 KAStarIncMOSPP — lifecycle + cross-algorithm cost-equivalence.

 The flip-to-OMSPP delegation must produce the SAME optimal
 per-start costs as the forward MOSPP solvers (AStarRepMOSPP
 ground truth, AStarIncMOSPP) on an undirected grid, and a
 nested run()+extend() must equal a fresh full run().
============================================================================
"""
import pytest

from f_hs.algo.i_1_mospp.i_1_kastar_inc import KAStarIncMOSPP
from f_hs.algo.i_1_mospp import AStarRepMOSPP
from f_hs.algo.i_1_mospp.i_1_astar_inc import AStarIncMOSPP
from f_hs.problem.i_1_grid import ProblemGrid


def _h(s, g) -> float:
    return float(s.distance(g))


def _costs_by_rc(algo) -> dict:
    """Per-start optimal costs keyed by (row, col) — comparable
    across separate problem instances."""
    return {(s.key.row, s.key.col): v.cost
            for s, v in algo.solutions.items()}


def test_costs_match_rep_ground_truth() -> None:
    """
    ========================================================================
     KAStarIncMOSPP (flip→OMSPP kA*_inc) must reproduce the
     AStarRepMOSPP baseline's per-start optimal costs exactly.
    ========================================================================
    """
    kinc = KAStarIncMOSPP.Factory.grid_6x6_zigzag_mospp()
    kinc.run()
    rep = AStarRepMOSPP(
        problem=ProblemGrid.Factory.grid_6x6_zigzag_mospp(), h=_h)
    rep.run()
    assert _costs_by_rc(kinc) == _costs_by_rc(rep)


def test_costs_match_astar_inc() -> None:
    """
    ========================================================================
     The two incremental MOSPP solvers (forward AStarIncMOSPP,
     flip KAStarIncMOSPP) agree on every per-start cost.
    ========================================================================
    """
    kinc = KAStarIncMOSPP.Factory.grid_6x6_zigzag_mospp()
    kinc.run()
    fwd = AStarIncMOSPP(
        problem=ProblemGrid.Factory.grid_6x6_zigzag_mospp(),
        h=_h, order_starts='given')
    fwd.run()
    assert _costs_by_rc(kinc) == _costs_by_rc(fwd)


def test_extend_equals_fresh_full_run() -> None:
    """
    ========================================================================
     run([first start]) + extend([rest]) yields the same
     per-start costs as a fresh run over all starts.
    ========================================================================
    """
    chained = KAStarIncMOSPP.Factory.grid_6x6_zigzag_mospp()
    starts = list(chained.problem.starts)
    chained.problem._starts = starts[:1]
    chained.run()
    chained.extend(starts[1:])

    fresh = KAStarIncMOSPP.Factory.grid_6x6_zigzag_mospp()
    fresh.run()
    assert _costs_by_rc(chained) == _costs_by_rc(fresh)


def test_graph_abc_two_starts_costs() -> None:
    """
    ========================================================================
     Undirected A--B--C, starts [A, B], goal C: cost(A,C)=2,
     cost(B,C)=1.
    ========================================================================
    """
    algo = KAStarIncMOSPP.Factory.graph_abc_two_starts()
    algo.run()
    costs = {s.key: v.cost for s, v in algo.solutions.items()}
    assert costs == {'A': 2.0, 'B': 1.0}


def test_requires_exactly_one_goal() -> None:
    """
    ========================================================================
     A problem with != 1 goal is rejected at construction.
    ========================================================================
    """
    p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
    p._goals = list(p.starts)  # >1 goal
    with pytest.raises(ValueError):
        KAStarIncMOSPP(problem=p, h=_h)


def test_extend_before_run_raises() -> None:
    """
    ========================================================================
     extend() before a completed run() is a RuntimeError.
    ========================================================================
    """
    algo = KAStarIncMOSPP.Factory.grid_6x6_zigzag_mospp()
    starts = list(algo.problem.starts)
    with pytest.raises(RuntimeError):
        algo.extend(starts[:1])
