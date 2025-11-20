from f_search.algos.i_1_spp.i_2_dijkstra.main import Dijkstra, ProblemSPP


class Factory:
    """
    ============================================================================
     Factory for creating Dijkstra algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> Dijkstra:
        """
        ========================================================================
         Return a Dijkstra algorithm with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return Dijkstra(problem=problem, verbose=True)

    @staticmethod
    def with_obstacles() -> Dijkstra:
        """
        ========================================================================
         Return a Dijkstra algorithm with a ProblemSPP with obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.with_obstacles()
        return Dijkstra(problem=problem)
