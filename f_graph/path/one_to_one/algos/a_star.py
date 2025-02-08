from f_graph.path.one_to_one.algo import AlgoOneToOne, Problem, Cache, State


class AStar(AlgoOneToOne):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 cache: Cache = None,
                 state: State = None,
                 is_shared: bool = False,
                 name: str = 'AStar'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              cache=cache,
                              state=state,
                              is_shared=is_shared,
                              name=name)
