from f_search.algos.i_0_base import AlgoSearch
from f_search.problems import ProblemSearch
from f_search.solutions import SolutionSearch
from f_search.ds.data import DataBestFirst
from f_search.ds.frontier import FrontierBase as Frontier
from f_search.ds.state import StateBase
from typing import Generic, TypeVar, Callable
from abc import abstractmethod

State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)
Solution = TypeVar('Solution', bound=SolutionSearch)

class AlgoBestFirst(Generic[Problem, Solution, State],
                    AlgoSearch[Problem, Solution]):

    def __init__(self,
                 problem: Problem,
                 make_frontier: Callable[[], Frontier[State]],
                 name: str = 'AlgoBestFirst') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._data = DataBestFirst(make_frontier=make_frontier)

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Search should continue (if Frontier is not empty).
        ========================================================================
        """
        return bool(self._data.frontier)

    def _select_best(self) -> None:
        """
        ========================================================================
         Update the Best-State.
        ========================================================================
        """
        data = self._data
        data.best = data.frontier.pop()
    
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
        successors = self.problem.successors(state=data.best)
        # Handle Successors
        for succ in successors:
            if succ in data.explored:
                continue
            self._handle_successor(succ=succ)
            
    @abstractmethod
    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        pass
