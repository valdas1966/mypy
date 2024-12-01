from f_graph.path_finding.nodes.i_1_path import NodePath
from typing import Protocol, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Ops(Protocol[Node]):
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
