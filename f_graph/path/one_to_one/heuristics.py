from f_graph.path.node import NodePath as Node
from typing import Callable


class Heuristic(Callable[[Node, Node], int]):
    """
    ============================================================================
     Func of Heuristic-Distance from a given Node to a Goal.
    ============================================================================
    """

    def __init__(self,
                 heuristic: Callable[[Node, Node], int],
                 goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._heuristic = heuristic
        self._goal = goal

    def __call__(self, node: Node) -> int:
        """
        ========================================================================
         Return the Heuristic-Distance from a given Node to a Goal.
        ========================================================================
        """
        return self._heuristic(node, self._goal)
