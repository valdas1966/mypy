from f_search.algos.i_1_spp.i_1_bfs import BFS
from f_search.problems.i_1_spp import ProblemSPP
from f_search.ds.data import DataBestFirst


class Factory:
    """
    ============================================================================
     Factory for creating BFS algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> BFS:
        """
        ========================================================================
         Return a BFS algorithm with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return BFS(problem=problem)

    @staticmethod
    def without_obstacles_with_cell_00() -> BFS:
        """
        ========================================================================
         Return a BFS algorithm with a ProblemSPP without obstacles and with an
          explored Cell(0,0).
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        data = DataBestFirst.Factory.cell_00()
        return BFS(problem=problem, data=data)
