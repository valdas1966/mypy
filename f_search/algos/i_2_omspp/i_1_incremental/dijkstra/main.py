from f_search.algos.i_1_spp import Dijkstra
from f_search.algos.i_2_omspp.i_1_incremental import IncrementalOMSPP
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class DijkstraIncremental(IncrementalOMSPP):
    """
    ============================================================================
     Dijkstra Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================    
    """ 
    
    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'DijkstraIncremental') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        IncrementalOMSPP.__init__(self,
                                 problem=problem,
                                 type_algo=Dijkstra,
                                 name=name)
