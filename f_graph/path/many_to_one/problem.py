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
    def starts(self) -> set[Node]:
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
         Order the list by the distance to the goal (the farthest first).
        ========================================================================
        """
        # Create a dict that maps each Start to its Distance to the Goal
        distances: dict[Node, int] = dict()
        for start in self._starts:
            distances[start] = self.graph.distance(node_a=start,
                                                   node_b=self._goal)
        # Create a sorted list (reversed) of the starts by their distances
        starts_sorted: list[Node] = sorted(distances.items(),
                                           key=lambda item: item[1],
                                           reverse=True)
        # Create a list of One-to-One problems
        problems: list[ProblemOneToOne] = list()
        for start, _ in starts_sorted:
            problems.append(ProblemOneToOne(graph=self.graph,
                                            start=start,
                                            goal=self._goal))
        return problems

