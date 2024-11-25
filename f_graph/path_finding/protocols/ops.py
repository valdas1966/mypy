from f_graph.nodes.i_1_path import NodePath
from f_graph.path_finding.protocols.problem import Problem
from f_graph.path_finding.protocols.data import Data
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
