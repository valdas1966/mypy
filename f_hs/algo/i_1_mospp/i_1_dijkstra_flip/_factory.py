from f_hs.algo.i_1_mospp.i_1_dijkstra_flip.main import DijkstraFlipMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph


class Factory:
    """
    ============================================================================
     Factory for DijkstraFlipMOSPP test instances.
    ============================================================================
    """

    @staticmethod
    def graph_abc_two_starts() -> DijkstraFlipMOSPP:
        """
        ========================================================================
         k-Dijkstra-MOSPP on A -> B -> C (undirected) with
         starts [A, B], goal C. Cost(A,C)=2, cost(B,C)=1.
         Single inner Dijkstra pass from C observes B first
         (g=1) then A (g=2).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['A', 'C'], 'C': ['B']},
            start='A', goal='C',
        )
        p._starts = [p._states['A'], p._states['B']]
        p._goals = [p._states['C']]
        return DijkstraFlipMOSPP(problem=p)

    @staticmethod
    def graph_abc_repeated_start() -> DijkstraFlipMOSPP:
        """
        ========================================================================
         k-Dijkstra-MOSPP on A -> B (undirected) with starts
         [A, A], goal B. Duplicate start collapses to one
         solution entry, two `on_start` events.
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['A']},
            start='A', goal='B',
        )
        p._starts = [p._states['A'], p._states['A']]
        p._goals = [p._states['B']]
        return DijkstraFlipMOSPP(problem=p)
