from f_graph.algos.one_to_one.i_1_cache import (AlgoOneToOneCache, Problem,
                                                Data, OpsNode, Node)
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS_CACHE(AlgoOneToOneCache[Problem, Data, OpsNode, Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Cache object.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[Node],
                 name: str = 'BFS-CACHE') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOneCache.__init__(self,
                                   problem=problem,
                                   type_queue=QueueFIFO,
                                   cache=cache,
                                   name=name)
