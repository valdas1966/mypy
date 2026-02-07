from f_search.solutions.i_2_omspp.main import SolutionOMSPP, SolutionSPP
from f_search.ds.state import StateBase


class Factory:
    """
    ============================================================================
     Factory for SolutionOMSPP.
    ============================================================================
    """

    @staticmethod
    def invalid() -> SolutionOMSPP:
        """
        ========================================================================
         Factory of a valid solution.
        ========================================================================
        """
        sol_1 = SolutionSPP.Factory.valid()
        sol_2 = SolutionSPP.Factory.invalid()
        goal_1 = StateBase.Factory.a()
        goal_2 = StateBase.Factory.b()
        sub_solutions = {goal_1: sol_1, goal_2: sol_2}
        return SolutionOMSPP(subs=sub_solutions)
