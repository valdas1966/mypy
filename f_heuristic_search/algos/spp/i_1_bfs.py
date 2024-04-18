from f_heuristic_search.algos.spp.i_0_base import AlgoSPPBase, SPP, Node
from f_data_structure.collections.i_2_queue_fifo import QueueFIFO


class BFS(AlgoSPPBase[SPP, Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self,
                 spp: SPP) -> None:
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
