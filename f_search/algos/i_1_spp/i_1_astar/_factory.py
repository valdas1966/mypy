from f_search.algos.i_1_spp.i_1_astar.main import AStar
from f_search.problems import ProblemSPP
from f_search.ds.data import DataHeuristics


class Factory:
    """
    ============================================================================
     Factory for creating AStar algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return AStar(problem=problem)

    @staticmethod
    def with_obstacles() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemSPP with obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.with_obstacles()
        return AStar(problem=problem)

    @staticmethod
    def without_obstacles_with_cell_00() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemSPP without obstacles and with an
          explored Cell(0,0).
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        data = DataHeuristics.Factory.cell_00()
        return AStar(problem=problem, data=data)
