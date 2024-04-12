from f_heuristic_search.algos.spp.i_0_base import SPPAlgoBase
from f_heuristic_search.problem_types.spp.i_1_heuristics import SPPHeuristics
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell
from f_data_structure.collections.i_2_queue_priority import QueuePriority
from typing import TypeVar

SPP = TypeVar('SPP', bound=SPPHeuristics)
Node = TypeVar('Node', bound=NodeFCell)


class AStar(SPPAlgoBase[SPP, Node]):
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
        SPPAlgoBase.__init__(self, spp=spp, type_queue=QueuePriority)

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
