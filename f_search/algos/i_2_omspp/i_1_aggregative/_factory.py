from f_search.algos.i_2_omspp.i_1_aggregative.main import AStarAggregative
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for A* Aggregative Algorithm.
    ============================================================================
    """
    
    @staticmethod
    def without_obstacles() -> AStarAggregative:
        """
        ========================================================================
         Create an A* Aggregative Algorithm for the given Problem.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarAggregative(problem=problem)
    