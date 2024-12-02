from f_graph.graphs.i_0_base import GraphBase, NodeGraph
from typing import Protocol, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeGraph)


class Problem(Protocol[Graph, Node]):
    """
    ============================================================================
     Protocol of Path-Problems in Graphs.
    ============================================================================
    """

    @property
    def graph(self) -> Graph:
        """
        ========================================================================
         Return a Graph of the Problem.
        ========================================================================
        """

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start-Node of the Problem.
        ========================================================================
        """

    @property
    def goals(self) -> set[Node]:
        """
        ========================================================================
         Return the Goal-Nodes of the Problem.
        ========================================================================
        """

    def get_children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return a List of Node's Neighbors in the Graph.
        ========================================================================
        """
