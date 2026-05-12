from f_hs.algo.i_1_omspp.i_1_kxastar.main import KxAStarOMSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ============================================================================
     Factory for KxAStarOMSPP test instances.
    ============================================================================
    """

    @staticmethod
    def graph_abc_two_goals() -> KxAStarOMSPP:
        """
        ========================================================================
         k×A* on A -> B -> C with goals [B, C]. Two independent
         sub-searches: sub-search 1 reaches B (cost 1);
         sub-search 2 starts from scratch (no shared state),
         reaches C (cost 2).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['C']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KxAStarOMSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )

    @staticmethod
    def graph_abc_repeated_goal() -> KxAStarOMSPP:
        """
        ========================================================================
         k×A* on A -> B -> C with goals [B, B]. Sub-search 1
         expands and reaches B (cost 1); sub-search 2 hits
         the already_reached fast-path — NO A* runs.
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['B']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KxAStarOMSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )
