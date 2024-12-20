from __future__ import annotations
from f_graph.path.data.problem import ProblemPath, dataclass
from f_graph.path.elements.graph import GraphPath
from f_graph.path.elements.node import NodePath
from f_graph.elements.graphs.u_2_grid import UGraphGrid
from typing import Generic, TypeVar, Type

Graph = TypeVar('Graph', bound=GraphPath)
Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class ProblemSingle(Generic[Graph, Node], ProblemPath[Graph, Node]):
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

    @classmethod
    def gen_3x3(cls, type_node: Type[Node] = NodePath) -> ProblemSingle:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 3x3 dimension.
        ========================================================================
        """
        graph = UGraphGrid.gen_3x3(type_node=type_node)
        start = graph[0, 0]
        goal = graph[2, 2]
        return ProblemSingle(graph=graph, start=start, goal=goal)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'{self.graph._grid.shape()}, {self.start} -> {self.goal}'
