from f_graph.algos.one_to_one.i_1_core import AlgoOneToOneCore, Problem, Node
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(AlgoOneToOneCore[Problem, Node]):
    """
    ============================================================================
     Breadth-First-Search Core-Algorithm.
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
        AlgoOneToOneCore.__init__(self,
                                  problem=problem,
                                  type_queue=QueueFIFO,
                                  name=name)
