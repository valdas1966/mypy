from __future__ import annotations
from f_graph.problem import ProblemGraph, dataclass
from f_graph.path.graph import GraphPath, NodePath
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphPath)
Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class ProblemPath(ProblemGraph[Graph, Node]):
    """
    ============================================================================
     Graph Path-Finding Problem class in Grid-Domain.
    ============================================================================
    """
    start: Node
    goals: set[Node]

    def clone(self) -> ProblemPath:
        """
        ========================================================================
         Return a Cloned problem.
        ========================================================================
        """
        graph = self.graph.clone()
        start = graph.node_from_uid(uid=self.start.uid)
        goals = {graph.node_from_uid(uid=goal.uid) for goal in self.goals}
        return ProblemPath(graph=graph, start=start, goals=goals)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'{self.graph._grid.shape()}, {self.start} -> {self.goals}'
