from f_ai.hs.heuristics.i_0_base import HeuristicsBase
from f_ai.hs.nodes.i_1_f_cell import NodeFCell
from typing import TypeVar, Callable

Node = TypeVar('Node', bound=NodeFCell)


class HeuristicsManhattan(HeuristicsBase[Node]):
    """
    ============================================================================
     Heuristics represented Manhattan-Distance between Node and Goal.
    ============================================================================
    """

    def __init__(self,
                 distance: Callable[[Node, Node], bool],
                 goal: Node) -> None:
        self._distance = distance
        self._goal = goal

    def eval(self, node: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance from Node to Goal.
        ========================================================================
        """
        return self._distance(node, self._goal)
