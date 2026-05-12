from f_hs.algo.i_1_mospp.i_1_kxastar.main import KxAStarMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ============================================================================
     Factory for KxAStarMOSPP test instances.
    ============================================================================
    """

    @staticmethod
    def graph_abc_two_starts() -> KxAStarMOSPP:
        """
        ========================================================================
         kxA*-MOSPP on A -> B -> C with starts [A, B], goal C.
         Two independent sub-searches: from A (cost 2), from B
         (cost 1).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='C',
        )
        p._starts = [p._states['A'], p._states['B']]
        p._goals = [p._states['C']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KxAStarMOSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )

    @staticmethod
    def graph_abc_repeated_start() -> KxAStarMOSPP:
        """
        ========================================================================
         kxA*-MOSPP on A -> B -> C with starts [A, A], goal B.
         Sub-search 1 expands and finalizes A (cost 1);
         sub-search 2 hits the already_reached fast-path.
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._starts = [p._states['A'], p._states['A']]
        p._goals = [p._states['B']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KxAStarMOSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )
