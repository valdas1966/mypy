from f_graph.path.single.algo import AlgoSingle, Problem, State, Node
from f_ds.queues.i_1_priority import QueuePriority


class AStar(AlgoSingle):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    type_queue = QueuePriority

    def __init__(self,
                 problem: Problem,
                 state: State = None,
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
                            state=state,
                            cache=cache,
                            heuristic=heuristic,
                            type_queue=AStar.type_queue,
                            name=name)
