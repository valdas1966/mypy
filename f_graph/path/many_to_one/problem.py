from f_graph.path.problem import ProblemPath, Graph, Node
from f_graph.path.one_to_one.problem import ProblemOneToOne
from typing import Iterable


class ProblemManyToOne(ProblemPath):
    """
    ============================================================================
     Problem-Class for Many-to-One Path-Finding Problems.
    ============================================================================
    """

    def __init__(self, graph: Graph, starts: Iterable[Node], goal: Node):
        """
        ========================================================================
         Constructor.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        self._starts = set(starts)
        self._goal = goal

    @property
    def starts(self):
        """
        ========================================================================
         Getter for the start-Nodes.
        ========================================================================
        """
        return self._starts
    
    @property
    def goal(self):
        """
        ========================================================================
         Getter for the goal-Node.
        ========================================================================
        """
        return self._goal

    def to_singles(self) -> list[ProblemOneToOne]:
        """
        ========================================================================
         Convert the Many-to-One problem to a list of One-to-One problems.
        ========================================================================
        """
        return [ProblemOneToOne(graph=self.graph, start=start, goal=self.goal)
                for start in self.starts]
