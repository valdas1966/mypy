from f_graph.path.one_to_one.algo import AlgoOneToOne, Problem
from f_graph.path.one_to_one.cache import Cache, Node
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoOneToOne):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Single-Goal.
    ============================================================================
    """

    type_queue = QueueFIFO

    def __init__(self,
                 problem: Problem,
                 cache: Cache = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              cache=cache,
                              type_queue=BFS.type_queue,
                              name='BFS')
