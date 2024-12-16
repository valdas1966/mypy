from f_graph.path.single.algo import AlgoSingle, Node
from f_graph.path.single.data.problem import ProblemSingle as Problem
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoSingle[Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[Node]):
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
