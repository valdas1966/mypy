from __future__ import annotations
from f_graph.path.problem import ProblemPath
from f_graph.path.elements.graph import GraphPath as Graph
from f_graph.path.elements.node import NodePath as Node
from typing import Type


class ProblemSingle(ProblemPath):
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
        ProblemPath.__init__(self, graph=graph, start=start)
        self._goal = goal

    @property
    def goal(self) -> Node:
        """
        ========================================================================
         Return the Goal of the Problem.
        ========================================================================
        """
        return self._goal

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
    def gen_3x3(cls, type_node: Type[Node] = Node) -> ProblemSingle:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 3x3 dimension.
        ========================================================================
        """
        graph = Graph.gen_3x3(type_node=type_node)
        start = graph[0, 0]
        goal = graph[2, 2]
        return ProblemSingle(graph=graph, start=start, goal=goal)

    @classmethod
    def gen_4x4(cls, type_node: Type[Node] = Node) -> ProblemSingle:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 4x4 dimension.
        ========================================================================
        """
        graph = Graph.gen_4x4(type_node=type_node)
        start = graph[0, 0]
        goal = graph[0, 3]
        return ProblemSingle(graph=graph, start=start, goal=goal)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid Path-Finding Problem.
        ========================================================================
        """
        return f'{self.graph._grid.shape()}, {self.start} -> {self.goal}'
