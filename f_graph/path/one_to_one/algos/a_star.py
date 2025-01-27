from f_graph.path.one_to_one.algo import AlgoOneToOne, Problem
from f_graph.path.one_to_one.cache import Cache
from f_graph.path.one_to_one.generators.g_heuristic import GenHeuristic
from f_ds.queues.i_1_priority import QueuePriority


class AStar(AlgoOneToOne):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    type_queue = QueuePriority

    def __init__(self,
                 problem: Problem,
                 cache: Cache = None,
                 name: str = 'AStar'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        heuristic = GenHeuristic.gen_manhattan(problem=problem)
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              cache=cache,
                              heuristic=heuristic,
                              type_queue=AStar.type_queue,
                              name=name)
