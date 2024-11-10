from f_graph.graphs.i_0_base import GraphBase, NodeBase
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeBase)


class ProblemGraph(Generic[Graph, Node]):
    """
    ============================================================================
     Base-Class for Graph-Problems in Computer Science.
    ============================================================================
    """

    def __init__(self, graph: Graph[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._graph = graph

    @property
    def graph(self) -> Graph[Node]:
        return self._graph
