from f_graph.path.single.algo import AlgoSingle, Problem, Node
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoSingle):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[Node] = None):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSingle.__init__(self,
                            problem=problem,
                            cache=cache,
                            type_queue=QueueFIFO,
                            name='BFS')
