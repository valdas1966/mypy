from f_hs.algo.i_1_omspp.i_2_kdijkstra.main import KDijkstra
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ========================================================================
     Factory for KDijkstra test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_two_goals() -> KDijkstra:
        """
        ====================================================================
         k-Dijkstra on A -> B -> C with goals [B, C]. Sub-search 1
         reaches B (cost 1); sub-search 2 resumes from shared
         state and reaches C (cost 2). h≡0 throughout.
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['C']]
        return KDijkstra(problem=p)

    @staticmethod
    def graph_abc_cached_at_b_first() -> KDijkstra:
        """
        ====================================================================
         k-Dijkstra on A -> B -> C with goals [C, B]. Sub-search 1
         expands A and B en route to C; sub-search 2 hits the
         already_closed fast-path for B.
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='C',
        )
        p._goals = [p._states['C'], p._states['B']]
        return KDijkstra(problem=p)
