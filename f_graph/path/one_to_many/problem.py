from f_graph.path.problem import ProblemPath, Graph, Node
from f_core.mixins.equable import Equable
from typing import Iterable


class ProblemOneToMany(ProblemPath, Equable):
    """
    ===========================================================================
     Problem for One-To-Many Pathfinding.
    ===========================================================================
    """

    def __init__(self, graph: Graph, start: Node, goals: Iterable[Node]):
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        self._start = start
        self._goals = set(goals)

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start of the Problem.
        ========================================================================
        """
        return self._start  

    @property
    def goals(self) -> set[Node]:
        """
        ========================================================================
         Return the Goals of the Problem.
        ========================================================================
        """
        return self._goals

    def clone(self) -> 'ProblemOneToMany':
        """
        ========================================================================
         Clone the Problem.
        ========================================================================
        """
        graph = self.graph.clone()
        start = graph.node(uid=self.start.uid)
        goals = set(graph.node(uid=goal.uid) for goal in self.goals)
        return ProblemOneToMany(graph=graph, start=start, goals=goals)  
    
    def key_comparison(self) -> tuple[Graph, Node, set[Node]]:
        """
        ========================================================================
         Compare by a Tuple of (Graph, Start, Goals).
        ========================================================================
        """
        return self.graph, self.start, self.goals

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'ProblemOneToMany(graph={self.graph._grid.shape()},' \
               f' start={self.start}, goals={self.goals})'
