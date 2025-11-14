from f_search.algos.i_1_omspp.i_1_kxastar.main import KxAStar, ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for creating KxAStar algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> KxAStar:
        """
        ========================================================================
         Return a KxAStar algorithm with a ProblemOMSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return KxAStar(problem=problem, verbose=True)

    @staticmethod
    def with_obstacles() -> KxAStar:
        """
        ========================================================================
         Return a KxAStar algorithm with a ProblemOMSPP with obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.with_obstacles()
        return KxAStar(problem=problem)
