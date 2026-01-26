from f_search.algos.i_1_spp.i_1_bfs import BFS
from f_search.problems.i_1_spp import ProblemSPP

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
