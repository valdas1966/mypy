from f_search.algos.i_0_base import AlgoSearch
from f_search.problems import ProblemSearch, State
from f_search.solutions import SolutionSearch
from f_search.stats import StatsSearch
from f_search.ds.data import DataBestFirst
from f_search.ds.priority import PriorityG as Priority
from abc import abstractmethod
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)
Stats = TypeVar('Stats', bound=StatsSearch)
Data = TypeVar('Data', bound=DataBestFirst)


class AlgoBestFirst(Generic[Problem, Solution, Stats, Data],
                    AlgoSearch[Problem, Solution, Stats, Data]):
    """
    ============================================================================
     Base for Best-First Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 name: str = 'AlgoBestFirst') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            data=data,
                            name=name)

    @abstractmethod
    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass     

    @abstractmethod
    def _create_solution(self, is_valid: bool) -> Solution:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        pass
    
    @abstractmethod
    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should terminate.
        ========================================================================
        """
        pass

    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the Best-State.
        ========================================================================
        """
        self._stats.explored += 1
        # Aliases
        data = self._data
        # Add State to Explored
        data.explored.add(data.best)
        # Get the Successors of the Best-State
        successors = self._problem.successors(state=data.best)
        # Operate Successors
        for succ in successors:
            # If the Successor is already explored, skip it
            if succ in data.explored:
                continue
            # If the Successor is not in the Frontier, discover it
            if succ not in data.frontier:
                self._discover(state=succ)
            # If the Successor is in the Frontier, relax it if needed
            else:   
                if self._need_relax(state=succ):
                    self._relax(state=succ)

    def _discover(self, state: State) -> None:
        """
        ========================================================================
         Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1

    @abstractmethod
    def _need_relax(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the given State needs to be relaxed.
        ========================================================================
        """
        pass

    def _relax(self, state: State) -> None:
        """
        ========================================================================
         Relax the given State.
        ========================================================================
        """
        self._stats.relaxed += 1

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Search should continue.
        ========================================================================
        """
        return self._data.frontier

    def _update_best(self) -> None:
        """
        ========================================================================
         Update the Best-State.
        ========================================================================
        """
        data = self._data
        data.best = data.frontier.pop()
