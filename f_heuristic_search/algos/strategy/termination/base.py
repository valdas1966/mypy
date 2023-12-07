from abc import ABC, abstractmethod
from f_heuristic_search.nodes.i_1_g import NodeG as Node


class TerminationBase(ABC):
    """
    ============================================================================
     Abstract Strategy for Search-Termination.
    ============================================================================
    """

    @abstractmethod
    def can_terminate(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Search can be Terminated.
        ========================================================================
        """
        pass
