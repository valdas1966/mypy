from f_heuristic_search.algos.spp.i_0_base import SPPAlgoBase
from f_heuristic_search.problem_types.spp.i_1_heuristics import SPPHeuristics
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell
from f_data_structure.collections.i_2_queue_priority import QueuePriority
from typing import TypeVar


Node = TypeVar('Node', bound=NodeFCell)


class AStar(SPPAlgoBase):
    """
    ============================================================================
     Base-Class for A* Algorithm.
    ============================================================================
    """

    def __init__(self, spp: SPPHeuristics) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SPPAlgoBase.__init__(spp=spp, type_queue=QueuePriority)

    def _process_child(self, child: Node, node: Node) -> None:
        """
        ========================================================================
         Generate a Child if it is not already generated.
        ========================================================================
        """
        if child in self.generated:
            child.update_parent_if_needed(parent=node)
        else:
            child.update_parent(parent=node)
            self._generate_node(node=child)
