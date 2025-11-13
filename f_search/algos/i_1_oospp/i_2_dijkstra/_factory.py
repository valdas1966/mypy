from f_search.algos.i_1_oospp.i_2_dijkstra.main import Dijkstra, ProblemOOSPP


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
         Return a Dijkstra algorithm with a ProblemOOSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOOSPP.Factory.without_obstacles()
        return Dijkstra(problem=problem, verbose=True)

    @staticmethod
    def with_obstacles() -> Dijkstra:
        """
        ========================================================================
         Return a Dijkstra algorithm with a ProblemOOSPP with obstacles.
        ========================================================================
        """
        problem = ProblemOOSPP.Factory.with_obstacles()
        return Dijkstra(problem=problem)
