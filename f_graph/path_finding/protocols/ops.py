from f_graph.nodes.i_1_path import NodePath
from typing import Protocol, TypeVar

Node = TypeVar('Node', bound=NodePath)


class ProtocolOps(Protocol[Node]):
    """
    ============================================================================
     Protocol of Operations object if Path-Finding Algorithms.
    ============================================================================
    """

    def generate(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node.
        ========================================================================
        """

    def explore(self, node: Node) -> None:
        """
        ========================================================================
         Explore a Node.
        ========================================================================
        """