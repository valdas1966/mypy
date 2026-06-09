from f_hs.algo.i_1_mospp.i_1_kastar_inc.main import KAStarIncMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


def _h_grid(s, g) -> float:
    """
    ============================================================================
     Manhattan heuristic for ProblemGrid StateCells (bi-arg
     `h(state, goal)`); symmetric, so valid under the flip.
    ============================================================================
    """
    return float(s.distance(g))


class Factory:
    """
    ============================================================================
     Factory for KAStarIncMOSPP test instances.
    ============================================================================
    """

    @staticmethod
    def grid_6x6_zigzag_mospp() -> KAStarIncMOSPP:
        """
        ========================================================================
         Canonical MOSPP grid: the `grid_6x6_zigzag_mospp`
         fixture (starts (0,0)/(2,3)/(0,3); goal (5,0)) shared
         with the `AStarIncMOSPP` oracle, so the two incremental
         MOSPP solvers can be cost-cross-checked on identical
         input. Undirected uniform-weight grid — the flip is
         exact.
        ========================================================================
        """
        return KAStarIncMOSPP(
            problem=ProblemGrid.Factory.grid_6x6_zigzag_mospp(),
            h=_h_grid,
        )

    @staticmethod
    def graph_abc_two_starts() -> KAStarIncMOSPP:
        """
        ========================================================================
         kA*_inc-MOSPP on undirected A--B--C with starts [A, B],
         goal C. Cost(A,C)=2, cost(B,C)=1. One inner OMSPP search
         grows from C outward, reaching B then A.
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['A', 'C'], 'C': ['B']},
            start='A', goal='C',
        )
        p._starts = [p._states['A'], p._states['B']]
        p._goals = [p._states['C']]
        return KAStarIncMOSPP(problem=p, h=lambda s, g: 0)
