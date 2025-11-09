from f_cs.solution import SolutionAlgo
from f_search.stats import StatsSearch
from typing import Generic, TypeVar, Iterable
from f_search.state import State
from f_search.cost import Cost

Stats = TypeVar('Stats', bound=StatsSearch)


class SolutionSearch(Generic[Stats], SolutionAlgo[Stats]):
    """
    ============================================================================
     Solution for Search-Problems.
    ============================================================================
    """
    def __init__(self,
                 is_valid: bool,
                 stats: Stats,
                 generated: Iterable[State],
                 explored: set[State],
                 g: dict[State, int],
                 cost: dict[State, Cost]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=is_valid, stats=stats)
        self._generated = generated
        self._explored = explored
        self._g = g
        self._cost = cost

    @property
    def generated(self) -> Iterable[State]:
        """
        ========================================================================
         Return the Generated States.
        ========================================================================
        """
        return self._generated