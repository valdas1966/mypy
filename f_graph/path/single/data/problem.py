from __future__ import annotations
from f_graph.path.data.problem import ProblemPath, dataclass
from f_graph.path.elements.graph import GraphPath
from f_graph.path.elements.node import NodePath
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphPath)
Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class ProblemSingle(ProblemPath[Graph, Node]):
    """
    ============================================================================
     Path-Finding Problem with Single-Goal.
    ============================================================================
    """
    goal: Node

    def clone(self) -> ProblemSingle:
        """
        ========================================================================
         Return a Cloned problem.
        ========================================================================
        """
        graph = self.graph.clone()
        start = graph.node_from_uid(uid=self.start.uid)
        goal = graph.node_from_uid(uid=self.goal.uid)
        return ProblemSingle(graph=graph, start=start, goal=goal)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'{self.graph._grid.shape()}, {self.start} -> {self.goal}'
