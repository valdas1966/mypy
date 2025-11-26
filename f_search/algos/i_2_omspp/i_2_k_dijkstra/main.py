from f_search.algos.i_2_omspp.i_1_iterative.main import (IterativeOMSPP,
                                                         ProblemOMSPP)
from f_search.algos import Dijkstra


class KDijkstra(IterativeOMSPP):
    """
    ============================================================================
     K-Dijkstra Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    
    # Factory.
    Factory: type = None
    
    def __init__(self,
                 problem: ProblemOMSPP,
                 verbose: bool = False,
                 name: str = 'KDijkstra') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        IterativeOMSPP.__init__(self,
                                problem=problem,
                                type_algo=Dijkstra,
                                verbose=verbose,
                                name=name)
