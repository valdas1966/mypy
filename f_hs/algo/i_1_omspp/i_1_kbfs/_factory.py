from f_hs.algo.i_1_omspp.i_1_kbfs.main import KBFS
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ========================================================================
     Factory for KBFS test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_two_goals() -> KBFS:
        """
        ====================================================================
         k-BFS on A -> B -> C with goals [B, C]. Sub-search 1
         reaches B (depth 1); sub-search 2 resumes and reaches
         C (depth 2).
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['C']]
        return KBFS(problem=p)

    @staticmethod
    def graph_abc_cached_at_b_first() -> KBFS:
        """
        ====================================================================
         k-BFS on A -> B -> C with goals [C, B]. Sub-search 1
         reaches C (closes B en route); sub-search 2 hits the
         already_closed fast-path on B.
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='C',
        )
        p._goals = [p._states['C'], p._states['B']]
        return KBFS(problem=p)
