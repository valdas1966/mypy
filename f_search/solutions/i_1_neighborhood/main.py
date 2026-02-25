from f_search.solutions.i_0_base.main import SolutionSearch
from f_search.problems import ProblemNeighborhood
from f_search.ds.state import StateCell as State
from f_search.stats import StatsSearch as Stats


class SolutionNeighborhood(SolutionSearch):
    """
    ============================================================================
     Solution for Neighborhood Problem.
    ============================================================================
    """

    def __init__(self,
                 name_algo: str,
                 problem: ProblemNeighborhood,
                 neighborhood: set[State],
                 stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionSearch.__init__(self,
                                name_algo=name_algo,
                                problem=problem,
                                is_valid=True,
                                stats=stats)
        self._neighborhood = neighborhood

    @property
    def neighborhood(self) -> set[State]:
        """
        ========================================================================
         Return the Solution's Neighborhood.
        ========================================================================
        """
        return self._neighborhood
