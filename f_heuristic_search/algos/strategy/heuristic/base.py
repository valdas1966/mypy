from abc import ABC, abstractmethod
from f_heuristic_search.nodes.i_1_h import NodeH as Node


class HeuristicBase(ABC):
    """
    ============================================================================
     Abstract Strategy for a Node's Heuristic Estimation.
    ============================================================================
    """

    @abstractmethod
    def estimate(self, node: Node) -> int:
        """
        ========================================================================
         Return Node's Heuristic-Estimation.
        ========================================================================
        """
        pass
