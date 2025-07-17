from __future__ import annotations
from f_graph.path.problem import ProblemPath, Graph, Node
from f_graph.path.one_to_one.problem import ProblemOneToOne
from f_core.mixins.clonable import Clonable


class ProblemManyToOne(ProblemPath, Clonable):
    """
    ============================================================================
     Problem-Class for Many-to-One Path-Finding Problems.
    ============================================================================
    """

    def __init__(self, graph: Graph, starts: list[Node], goal: Node):
        """
        ========================================================================
         Constructor.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        self._goal = goal
        self._starts = self._get_sorted_starts(starts=starts)

    @property
    def starts(self) -> list[Node]:
        """
        ========================================================================
         Getter for the start-Nodes.
        ========================================================================
        """
        return self._starts
    
    @property
    def goal(self) -> Node:
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
        problems: list[ProblemOneToOne] = list()
        for start in self._starts:
            problems.append(ProblemOneToOne(graph=self.graph.clone(),
                                            start=start.clone(),
                                            goal=self._goal.clone()))
        return problems

    def clone(self) -> ProblemManyToOne:
        """
        ========================================================================
         Clone the Problem.
        ========================================================================
        """
        graph = self.graph.clone()
        starts = [start.clone() for start in self.starts]
        goal = self.goal.clone()
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)

    def _get_sorted_starts(self, starts: list[Node]) -> list[Node]:
        """
        ========================================================================
         Get the sorted starts by their distances to the goal (decreasing).
         Returns a list of Start-Nodes.
        ========================================================================
        """
        distances: dict[Node, int] = dict()
        for start in starts:
            distances[start] = self.graph.distance(node_a=start,
                                                   node_b=self._goal)
        tuples = sorted(distances.items(),
                        key=lambda item: item[1],
                        reverse=True)
        return [node for node, _ in tuples]
