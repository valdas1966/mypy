from f_heuristic_search.algos.spp.i_0_base import SPPAlgoBase, Node
from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_data_structure.collections.i_2_queue_fifo import QueueFIFO


class BFS(SPPAlgoBase):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self,
                 spp: SPPConcrete) -> None:
        """
        ========================================================================
         1. Init private Attributes.
         2. The Queue should be FIFO.
        ========================================================================
        """
        SPPAlgoBase.__init__(self,
                             spp=spp,
                             type_queue=QueueFIFO)

    def _process_child(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Generate a Child if it is not already generated.
        ========================================================================
        """
        if child not in self.generated:
            self._generate_node(node=child, parent=parent)
