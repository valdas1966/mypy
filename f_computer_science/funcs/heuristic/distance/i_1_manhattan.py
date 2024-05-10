# .. = f_computer_science.funcs.heuristi.distance
from ..distance.i_0_base import Heuristic
from f_data_structure.nodes.i_2_cell import NodeCell


class DistanceManhattan(Heuristic[NodeCell]):
    """
    ============================================================================
     Manhattan-Distance Heuristic-Function.
    ============================================================================
    """

    def __init__(self, goal: NodeCell) -> None:
        self._goal = goal

    def calc(self, node: NodeCell) -> int:
        """
        ========================================================================
         Return the Manhattan-Distance from Node to Goal.
        ========================================================================
        """
        return node.distance(other=self._goal)
