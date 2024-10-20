from f_graph.graphs.i_0_base import GraphBase, NodeBase
from typing import Generic, TypeVar
from abc import ABC

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeBase)


class ProblemGraph(ABC, Generic[Graph, Node]):
    """
    ============================================================================
     Base-Class for Graph-Problems in Computer Science.
    ============================================================================
    """

    def __init__(self, graph: Graph) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._graph = graph

    @property
    def graph(self) -> Graph:
        return self._graph
