from f_search.algos.i_2_omspp.i_1_incremental.bfs.main import BFSIncremental
from f_search.problems.i_2_omspp.main import ProblemOMSPP

class Factory:
    """
    ============================================================================
     Factory for Incremental BFS Algorithm for OMSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> BFSIncremental:
        """
        ========================================================================
         Return an Incremental BFS Algorithm for OMSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return BFSIncremental(problem=problem)
