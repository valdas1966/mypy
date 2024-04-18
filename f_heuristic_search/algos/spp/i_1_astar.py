from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_heuristic_search.algos.mixins.has_heuristics.i_1_spp import HasHeuristicsSPP
from f_heuristic_search.algos.spp.i_0_base import AlgoSPPBase
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell
from f_data_structure.collections.i_2_queue_priority import QueuePriority
from typing import TypeVar

SPP = TypeVar('SPP', bound=SPPConcrete)
Node = TypeVar('Node', bound=NodeFCell)


class AStar(AlgoSPPBase[SPP, Node], HasHeuristicsSPP[SPP, Node]):
    """
    ============================================================================
     Base-Class for A* Algorithm.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSPPBase.__init__(self, spp=spp, type_queue=QueuePriority)
        HasHeuristicsSPP.__init__(self, spp=spp)

    def _process_child(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Generate a Child if it is not already generated.
        ========================================================================
        """
        if child in self.generated:
            child.update_parent_if_needed(parent=parent)
        else:
            child.h = self.spp.calc_h(node=child)
            self._generate_node(node=child, parent=parent)

    def _generate_node(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         In addition to Generate_Node process in SPPAlgoBase (setting a parent
          and updating the g-value), set also a heuristic distance to Goal.
        ========================================================================
        """
        SPPAlgoBase._generate_node(self, node=node, parent=parent)
        node.h = self.spp.calc_h(node=node)
