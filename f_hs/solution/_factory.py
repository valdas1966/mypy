from f_hs.solution.main import SolutionSPP


class Factory:
    """
    ========================================================================
     Factory for SolutionSPP test instances.
    ========================================================================
    """

    @staticmethod
    def valid() -> SolutionSPP:
        """
        ====================================================================
         Create a valid SolutionSPP with cost 5.
        ====================================================================
        """
        return SolutionSPP(cost=5.0)

    @staticmethod
    def invalid() -> SolutionSPP:
        """
        ====================================================================
         Create an invalid SolutionSPP (no path found).
        ====================================================================
        """
        return SolutionSPP(cost=float('inf'))

    @staticmethod
    def zero() -> SolutionSPP:
        """
        ====================================================================
         Create a valid SolutionSPP with zero cost.
        ====================================================================
        """
        return SolutionSPP(cost=0.0)
