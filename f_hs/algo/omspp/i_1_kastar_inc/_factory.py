from f_hs.algo.omspp.i_1_kastar_inc.main import KAStarInc
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ========================================================================
     Factory for KAStarInc test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_two_goals() -> KAStarInc:
        """
        ====================================================================
         kA*_inc on A -> B -> C with goals [B, C]. Sub-search 1
         reaches B (cost 1); sub-search 2 resumes from shared
         state and reaches C (cost 2).
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['C']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KAStarInc(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )

    @staticmethod
    def graph_abc_cached_at_b_first() -> KAStarInc:
        """
        ====================================================================
         kA*_inc on A -> B -> C with goals [C, B]. Sub-search 1
         expands A and B on the way to C; sub-search 2 hits the
         already_closed fast-path for B.
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='C',
        )
        p._goals = [p._states['C'], p._states['B']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return KAStarInc(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
        )
