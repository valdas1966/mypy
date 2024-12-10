from f_graph.path.single.algo import AlgoPath, TProblem, TPath, TData, TOps, TNode
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoPath[TProblem, TPath, TData, TOps, TNode]):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: TProblem,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          type_queue=QueueFIFO,
                          name=name)
