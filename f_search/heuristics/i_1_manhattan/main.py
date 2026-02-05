from f_search.heuristics.i_0_base import HeuristicsBase
from f_search.problems.i_0_base import ProblemSearch
from f_search.ds.state import StateBase
from typing import TypeVar, Generic

Problem = TypeVar('Problem', bound=ProblemSearch)
State = TypeVar('State', bound=StateBase)


class HeuristicsManhattan(Generic[Problem, State], HeuristicsBase[Problem, State]):
    """
    ============================================================================
     Heuristics represented Manhattan-Distance between State and Goal.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        super().__init__(problem=problem)
    
    def __call__(self, state: State) -> int:
        """
        ========================================================================
         Return Manhattan-Distance between State and Goal.
        ========================================================================
        """
        return self._problem.goal.distance(other=state)
