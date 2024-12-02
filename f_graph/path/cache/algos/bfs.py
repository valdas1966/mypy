from f_graph.path.cache.algo import (AlgoCache, TProblem, TPath, TData,
                                     TOps, TNode)
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoCache[TProblem, TPath, TData, TOps, TNode]):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm with Cache object.
    ============================================================================
    """

    def __init__(self,
                 problem: TProblem,
                 cache: set[TNode],
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoCache.__init__(self,
                           problem=problem,
                           cache=cache,
                           type_queue=QueueFIFO,
                           name=name)
