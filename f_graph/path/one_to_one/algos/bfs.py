from f_graph.path.one_to_one.algo import (AlgoOneToOne, Problem, Cache, State,
                                          TypeQueue, TypeHeuristic)


class BFS(AlgoOneToOne):
    """
    ============================================================================
     Breadth-First-Search Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: Cache = None,
                 state: State = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              cache=cache,
                              state=state,
                              type_queue=TypeQueue.FIFO,
                              type_heuristic=TypeHeuristic.ZERO,
                              name='BFS')
