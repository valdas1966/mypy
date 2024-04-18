from f_heuristic_search.algos.mixins.has_heuristics.i_0_base import HasHeuristicsBase
from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)
SPP = TypeVar('SPP', bound=SPPConcrete)


class HasHeuristicsSPP(Generic[SPP, Node], HasHeuristicsBase[Node]):
    """
    ============================================================================
     Mixin-Class for SPP-Algos with Heuristics.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spp = spp

    def calc(self, node: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance between the given Node and the Goal.
        ========================================================================
        """
        return node.distance(other=self._spp.goal)
