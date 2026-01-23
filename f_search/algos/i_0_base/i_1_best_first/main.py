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
        # Aliases
        data = self._data
        stats = self._stats
        # Increment explored stats
        stats.explored += 1
        # Add State to Explored
        data.explored.add(data.best)
        # Generate State's unexplored Successors
        successors = self._problem.successors(state=data.best)
        for succ in successors:
            if succ in data.explored:
                continue
            if succ in data.frontier:
                self._relax(state=succ)
            else:   
                self._discover(state=succ)

    def _discover(self, state: State) -> None:
        """
        ========================================================================
         Discover a new state.
        ========================================================================
        """
        data = self._data
        data.dict_parent[state] = data.best
        data.dict_g[state] = data.dict_g[data.best] + 1 if data.best else 0
        data.dict_priority[state] = Priority(key=state,
                                                        g=data.dict_g[state])
        data.frontier.push(state=state, priority=data.dict_priority[state])
        self._stats.discovered += 1

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
