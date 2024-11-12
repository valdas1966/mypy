from f_graph.problems.i_0_graph import ProblemGraph, GraphBase
from f_graph.nodes.i_1_path import NodePath
from collections.abc import Collection
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)


class Problem(Generic[Graph, Node],
              ProblemGraph[Graph, Node]):
    """
    ============================================================================
     Graph-Path Problem.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph[Node],
                 start: Node,
                 goals: Collection[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemGraph.__init__(self, graph=graph)
        self._start = start
        self._goals = set(goals)

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start Node of the Problem.
        ========================================================================
        """
        return self._start

    @property
    def goals(self) -> set[Node]:
        """
        ========================================================================
         Return the Goals Nodes of the Problem.
        ========================================================================
        """
        return self._goals.copy()
