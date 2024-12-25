from f_graph.path.single.algo import AlgoSingle, Problem, State, Node
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoSingle):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Single-Goal.
    ============================================================================
    """

    type_queue = QueueFIFO

    def __init__(self,
                 problem: Problem,
                 state: State = None,
                 cache: set[Node] = None,
                 ):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSingle.__init__(self,
                            problem=problem,
                            state=state,
                            cache=cache,
                            type_queue=BFS.type_queue,
                            name='BFS')
