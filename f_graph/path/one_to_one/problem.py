from f_graph.path.problem import ProblemPath, Graph, Node
from f_core.mixins.equable import Equable


class ProblemOneToOne(ProblemPath, Equable):
    """
    ============================================================================
     Path-Finding Problem with Single-Goal.
    ============================================================================
    """

    def __init__(self, graph: Graph, start: Node, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        self._start = start
        self._goal = goal

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start of the Problem.
        ========================================================================
        """
        return self._start

    @property
    def goal(self) -> Node:
        """
        ========================================================================
         Return the Goal of the Problem.
        ========================================================================
        """
        return self._goal

    def clone(self) -> 'ProblemOneToOne':
        """
        ========================================================================
         Return a Cloned problem.
        ========================================================================
        """
        graph = self.graph.clone()
        start = graph.nodes_by_keys(key=self.start.key)
        goal = graph.nodes_by_keys(key=self.goal.key)
        return ProblemOneToOne(graph=graph, start=start, goal=goal)

    def reverse(self) -> 'ProblemOneToOne':
        """
        ========================================================================
         Return a Reversed version of the Problem.
        ========================================================================
        """
        problem = self.clone()
        return ProblemOneToOne(graph=problem.graph,
                               start=problem.goal,
                               goal=problem.start)

    def key_comparison(self) -> tuple[Graph, Node, Node]:
        """
        ========================================================================
         Compare by a Tuple of (Graph, Start, Goal).
        ========================================================================
        """
        return self.graph, self.start, self.goal

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'{self.graph.shape()}, {self.start} -> {self.goal}'
    