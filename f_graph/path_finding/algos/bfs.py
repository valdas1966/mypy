from f_graph.path_finding.algo import Algo, Problem, Path, Data, Ops, TNode
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(Algo[Problem, Path, Data, Ops, TNode]):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self,
                      problem=problem,
                      type_queue=QueueFIFO,
                      name=name)
