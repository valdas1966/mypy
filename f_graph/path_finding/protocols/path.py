from f_graph.nodes.i_1_path import NodePath
from typing import Protocol, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Path(Protocol[Node]):
    """
    ============================================================================
     Protocol for solutions of Path-Finding Algorithms (an optimal-path).
    ============================================================================
    """

    def get(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return an Optimal-Path from a Start-Node to a given Node.
        ========================================================================
        """