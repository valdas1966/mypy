from f_heuristic_search.algos.strategy.heuristic.base import HeuristicBase
from f_heuristic_search.nodes.i_1_h import NodeH as Node


class HeuristicManual(HeuristicBase):
    """
    ============================================================================
     Strategy for Heuristic-Estimation using a Lookup-Table.
    ============================================================================
    """

    def __init__(self, heuristics: dict[Node, int]) -> None:
        """
        ========================================================================
         Init the Private Attributes.
        ========================================================================
        """
        self._heuristics = heuristics

    def estimate(self, node: Node) -> int:
        """
        ========================================================================
         Return Node's Heuristic-Estimation using a Lookup-Table.
        ========================================================================
        """
        return self._heuristics[node]
