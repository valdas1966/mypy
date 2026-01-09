from f_search.algos.i_1_spp import AStar
from f_search.algos.i_2_omspp.i_1_incremental import IncrementalOMSPP
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class AStarIncremental(IncrementalOMSPP):
    """
    ============================================================================
     A* Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None
    
    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AStarIncremental') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, type_algo=AStar, name=name)
