from f_search.solutions import SolutionSearch
from f_search.solutions import SolutionSPP
from f_search.problems import ProblemOMSPP
from f_search.stats import StatsSearch
from f_search.ds.path import Path
from f_search.ds.state import StateBase as State


class SolutionOMSPP(SolutionSearch[ProblemOMSPP, StatsSearch]):
    """
    ============================================================================
     Solution for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 name_algo: str,
                 problem: ProblemOMSPP,
                 subs: list[SolutionSPP],
                 elapsed: int) -> None:
        """
        ========================================================================
         Init private Attributes.
         Stats are already accumulated by the algorithm during execution.
        ========================================================================
        """
        discovered = sum(sub.stats.discovered for sub in subs)
        explored = sum(sub.stats.explored for sub in subs)
        is_valid = all(sub for sub in subs) and len(subs) == len(problem.goals)
        stats = StatsSearch(elapsed=elapsed,
                            discovered=discovered,
                            explored=explored)
        SolutionSearch.__init__(self,
                                name_algo=name_algo,
                                problem=problem,
                                is_valid=is_valid,
                                stats=stats)
        self._subs = subs
        self._paths = {sub.problem.goal: sub.path for sub in subs}

    @property
    def paths(self) -> dict[State, Path]:
        """
        ========================================================================
         Return the Solution's Paths for Each Goal.
        ========================================================================
        """
        return self._paths

    @property
    def subs(self) -> list[SolutionSPP]:
        """
        ========================================================================
         Return the Sub-Solutions.
        ========================================================================
        """
        return self._subs
