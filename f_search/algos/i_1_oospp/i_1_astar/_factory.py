from f_search.algos.i_1_oospp.i_1_astar.main import AStar, ProblemOOSPP


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
         Return a AStar algorithm with a ProblemOOSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOOSPP.Factory.without_obstacles()
        return AStar(problem=problem, verbose=True)

    @staticmethod
    def with_obstacles() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemOOSPP with obstacles.
        ========================================================================
        """
        problem = ProblemOOSPP.Factory.with_obstacles()
        return AStar(problem=problem)
