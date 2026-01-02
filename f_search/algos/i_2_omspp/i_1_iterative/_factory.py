from f_search.algos.i_2_omspp.i_1_iterative.main import IterativeOMSPP as Algo
from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for IterativeOMSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles_4x4() -> Algo:
        """
        ========================================================================
         Return a IterativeOMSPP for a 4x4 grid without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        algo = Algo(problem=problem, type_algo=AStar)
        return algo
