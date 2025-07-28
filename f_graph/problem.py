from f_ds.old_graphs.i_0_base import GraphBase, NodeKey
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeKey)


class ProblemGraph(Generic[Graph, Node]):
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
        """
        ========================================================================
         Return the Problem's Graph.
        ========================================================================
        """
        return self._graph
