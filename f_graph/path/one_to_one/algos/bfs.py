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
                 state: State = None,
                 is_shared: bool = False) -> None:
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
                              is_shared=is_shared,
                              name='BFS')
