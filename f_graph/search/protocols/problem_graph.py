from f_graph.graphs.i_0_base import GraphBase, NodeBase
from typing import Protocol, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeBase)


class ProtocolProblemGraph(Protocol[Graph, Node]):
    """
    ============================================================================
     Protocol of Graph-Problems in Computer Science.
    ============================================================================
    """

    @property
    def graph(self) -> Graph:
        """
        ========================================================================
         Return a Graph of the Problem.
        ========================================================================
        """

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return a List of Node's Neighbors in the Graph.
        ========================================================================
        """