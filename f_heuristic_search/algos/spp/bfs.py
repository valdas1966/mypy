from f_heuristic_search.algos.spp.base import SPPAlgoBase
from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_data_structure.collections.queue_fifo import QueueFIFO
from f_data_structure.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class BFS(Generic[Node], SPPAlgoBase):
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

    def run(self) -> None:
        """
        ========================================================================
         Run the BFS Algo.
        ========================================================================
        """
        self._generate_node(node=self.spp.start)
        while self._generated:
            best = self._generated.pop()
            if best == self.spp.goal:
                self._is_path_found = True
                break
            self._expand_node(node=best)
