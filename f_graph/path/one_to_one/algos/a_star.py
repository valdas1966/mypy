from f_graph.path.one_to_one.algo import (AlgoOneToOne, Problem, State, Node,
                                          Callable)
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
                 state: State = None,
                 cache: dict[Node, Callable[[], list[Node]]] = None,
                 name: str = 'AStar'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        heuristic = lambda node: problem.graph.distance(node, problem.goal)
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              cache=cache,
                              heuristic=heuristic,
                              type_queue=AStar.type_queue,
                              name=name)
