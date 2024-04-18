from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class HeuristicsSpp(Generic[Node]):
    """
    ============================================================================
     Manage Heuristics for Shortest-Path-Problems.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal

    def calc(self, node: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance between the given Node and the Goal.
        ========================================================================
        """
        return node.distance(other=self._goal)
