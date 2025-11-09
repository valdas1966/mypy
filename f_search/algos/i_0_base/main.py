from f_cs.algo import Algo
from f_search.cost import Cost
from f_search.stats import StatsSearch
from f_search.problems import ProblemSearch, State
from f_search.solutions import SolutionSearch
from typing import Generic, TypeVar, Iterable
Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)


class AlgoSearch(Generic[Problem, Solution],
                 Algo[Problem, Solution]):
    """
    ============================================================================
     Base for Search-Algorithms.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'AlgoSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, verbose=verbose, name=name)

    def _run_pre(self) -> None:
        """
        ========================================================================
         Init data structures.
        ========================================================================
        """
        Algo._run_pre(self)
        # Priority Queue for Generated States
        self._generated: Iterable[State] = None
        # Set of Explored States
        self._explored = set[State]()
        # Mapping of State's Parent
        self._parent = dict[State, State]()
        # Mapping of State's G-Values
        self._g = dict[State, int]()
        # Mapping of State's H-Values
        self._h = dict[State, int]()
        # Mapping of State's Total-Costs
        self._cost = dict[State, Cost]()
        # Best current generated state
        self._best: State = None
        # Stats of the Algorithm
        self._stats: StatsSearch = None
