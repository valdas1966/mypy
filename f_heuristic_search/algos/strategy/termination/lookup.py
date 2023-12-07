from f_heuristic_search.algos.strategy.termination.base import TerminationBase
from f_heuristic_search.nodes.i_1_g import NodeG as Node


class TerminationLookup(TerminationBase):
    """
    ============================================================================
     Strategy for Search-Termination using a Lookup-Table.
    ============================================================================
    """

    def __init__(self, lookup: dict[Node, int]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._lookup = lookup

    def can_terminate(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node is in the Lookup-Table.
        ========================================================================
        """
        return node in self._lookup
