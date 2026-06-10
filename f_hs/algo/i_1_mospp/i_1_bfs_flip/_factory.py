from f_hs.algo.i_1_mospp.i_1_bfs_flip.main import BFSFlipMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ============================================================================
     Factory for BFSFlipMOSPP test instances.
    ============================================================================
    """

    @staticmethod
    def graph_abc_two_starts() -> BFSFlipMOSPP:
        """
        ========================================================================
         k-BFS-MOSPP on A -> B -> C (undirected via the
         underlying graph builder) with starts [A, B], goal C.
         Cost(A,C)=2, cost(B,C)=1. Single inner BFS pass from
         C observes B first (depth 1) then A (depth 2).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['A', 'C'], 'C': ['B']},
            start='A', goal='C',
        )
        p._starts = [p._states['A'], p._states['B']]
        p._goals = [p._states['C']]
        return BFSFlipMOSPP(problem=p)

    @staticmethod
    def graph_abc_repeated_start() -> BFSFlipMOSPP:
        """
        ========================================================================
         k-BFS-MOSPP on A -> B (undirected) with starts [A, A],
         goal B. Single inner BFS pass; duplicate start collapses
         to one solution entry, two `on_start` events (one per
         duplicate index).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['A']},
            start='A', goal='B',
        )
        p._starts = [p._states['A'], p._states['A']]
        p._goals = [p._states['B']]
        return BFSFlipMOSPP(problem=p)
