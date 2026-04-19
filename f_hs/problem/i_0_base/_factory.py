from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase


class _ProblemGraph(ProblemSPP[StateBase[str]]):
    """
    ========================================================================
     Concrete ProblemSPP for testing with Graph Adjacency.
     Edge weights default to 1.0; pass `weights={(parent_key,
     child_key): w}` to override per-edge (any unspecified edge
     stays at 1.0).
    ========================================================================
    """

    def __init__(self,
                 adj: dict[str, list[str]],
                 start: str,
                 goal: str,
                 weights: dict[tuple[str, str], float] | None = None,
                 name: str = 'ProblemGraph') -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._adj = adj
        self._weights: dict[tuple[str, str], float] = weights or {}
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

    def w(self,
          parent: StateBase[str],
          child: StateBase[str]) -> float:
        """
        ====================================================================
         Return the Edge Cost. Falls back to the inherited default
         (1.0) when no per-edge weight was supplied.
        ====================================================================
        """
        return self._weights.get((parent.key, child.key), 1.0)


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

    @staticmethod
    def graph_decrease() -> ProblemSPP[StateBase[str]]:
        """
        ====================================================================
         Smallest weighted graph that forces a `decrease_g` event.

             S --1--> A --1--> X
              \\               ^
               1              0
                \\            /
                 v          /
                  B --------

         Adjacency `S: [A, B]` ensures A is pushed (and popped)
         before B. A then pushes X with g=2 via edge w(A,X)=1.
         When B pops next, it offers a strictly better path to X:
         new_g = g(B) + w(B,X) = 1 + 0 = 1 < g[X] = 2 — which
         triggers `decrease_g` and re-parents X from A to B.
         Optimal cost: 1 (S -> B -> X).

         Identical event order across BFS / Dijkstra / AStar
         (h=0): A pops first by FIFO (BFS) or by State tiebreak
         on ties (Dijkstra / AStar).
        ====================================================================
        """
        adj = {'S': ['A', 'B'], 'A': ['X'],
               'B': ['X'], 'X': []}
        weights = {('S', 'A'): 1.0, ('S', 'B'): 1.0,
                   ('A', 'X'): 1.0, ('B', 'X'): 0.0}
        return _ProblemGraph(adj=adj, start='S', goal='X',
                             weights=weights)
