from f_graph.path_finding.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Path(Generic[Node]):
    """
    ============================================================================
     Path object (the output) of Path-Algorithms.
    ============================================================================
    """

    def get(self, goal: Node) -> list[Node]:
        """
        ========================================================================
         Return an Optimal-Path from Start to the received Goal.
        ========================================================================
        """
        return goal.path_from_start()
