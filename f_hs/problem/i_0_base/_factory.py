from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase


class _ProblemGraph(ProblemSPP[StateBase[str]]):
    """
    ========================================================================
     Concrete ProblemSPP for testing with Graph Adjacency.
    ========================================================================
    """

    def __init__(self,
                 adj: dict[str, list[str]],
                 start: str,
                 goal: str,
                 name: str = 'ProblemGraph') -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._adj = adj
        self._states: dict[str, StateBase[str]] = {
            k: StateBase[str](key=k) for k in adj
        }
        ProblemSPP.__init__(
            self,
            starts=[self._states[start]],
            goals=[self._states[goal]],
            name=name,
        )

    def successors(self,
                   state: StateBase[str]
                   ) -> list[StateBase[str]]:
        """
        ====================================================================
         Return the Successors of the given State.
        ====================================================================
        """
        return [self._states[k]
                for k in self._adj.get(state.key, [])]


class Factory:
    """
    ========================================================================
     Factory for ProblemSPP test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc() -> ProblemSPP[StateBase[str]]:
        """
        ====================================================================
         Linear Graph: A -> B -> C (cost 2).
        ====================================================================
        """
        adj = {'A': ['B'], 'B': ['C'], 'C': []}
        return _ProblemGraph(adj=adj, start='A', goal='C')

    @staticmethod
    def graph_no_path() -> ProblemSPP[StateBase[str]]:
        """
        ====================================================================
         No Path: A -> B, C isolated.
        ====================================================================
        """
        adj = {'A': ['B'], 'B': [], 'C': []}
        return _ProblemGraph(adj=adj, start='A', goal='C')

    @staticmethod
    def graph_start_is_goal() -> ProblemSPP[StateBase[str]]:
        """
        ====================================================================
         Start equals Goal: A.
        ====================================================================
        """
        adj = {'A': ['B'], 'B': []}
        return _ProblemGraph(adj=adj, start='A', goal='A')

    @staticmethod
    def graph_diamond() -> ProblemSPP[StateBase[str]]:
        """
        ====================================================================
         Diamond: A -> B -> D, A -> C -> D (cost 2).
        ====================================================================
        """
        adj = {'A': ['B', 'C'], 'B': ['D'],
               'C': ['D'], 'D': []}
        return _ProblemGraph(adj=adj, start='A', goal='D')
