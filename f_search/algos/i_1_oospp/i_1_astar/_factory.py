from f_search.algos.i_1_oospp.i_1_astar import AStar, ProblemOOSPP, SolutionOOSPP



class Factory:
    """
    ============================================================================
     Factory for creating AStar algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> SolutionOOSPP:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemOOSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOOSPP.Factory.without_obstacles()
        return AStar.Factory.run(problem=problem)