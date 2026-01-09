from f_search.algos.i_2_omspp.i_1_repeated.astar.main import AStarRepeated
from f_search.problems.i_2_omspp import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for creating KxAStar algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> AStarRepeated:
        """
        ========================================================================
         Return a KxAStar algorithm with a ProblemOMSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarRepeated(problem=problem)

    @staticmethod
    def with_obstacles() -> AStarRepeated:
        """
        ========================================================================
         Return a KxAStar algorithm with a ProblemOMSPP with obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.with_obstacles()
        return AStarRepeated(problem=problem)
