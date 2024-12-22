from f_graph.path.single.algo import AlgoSingle, Problem, Node
from f_ds.queues.i_1_priority import QueuePriority


class AStar(AlgoSingle):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: set[Node] = None,
                 name: str = 'AStar'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        heuristic = lambda node: problem.graph.distance(node, problem.goal)
        AlgoSingle.__init__(self,
                            problem=problem,
                            cache=cache,
                            heuristic=heuristic,
                            type_queue=QueuePriority,
                            name=name)
