from f_graph.path.node import NodePath as Node
from typing import Callable


class Heuristic(Callable[[Node], int]):
    """
    ============================================================================
     Func of Heuristic-Distance from a given Node to a Goal.
    ============================================================================
    """

    def __init__(self, heuristic: Callable[[Node], int]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._heuristic = heuristic

    def __call__(self, node: Node) -> int:
        """
        ========================================================================
         Return the Heuristic-Distance from a given Node to a Goal.
        ========================================================================
        """
        return self._heuristic(node)