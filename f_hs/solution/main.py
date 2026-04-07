from f_cs.solution import SolutionAlgo


class SolutionSPP(SolutionAlgo):
    """
    ========================================================================
     Solution for Shortest-Path-Problem.
    ========================================================================
    """

    def __init__(self, cost: float) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=cost < float('inf'))
        self._cost = cost

    @property
    def cost(self) -> float:
        """
        ========================================================================
         Return the Path Cost.
        ========================================================================
        """
        return self._cost
