from f_search.algos.i_0_base import AlgoSearch
from f_search.problems import ProblemSearch, State
from f_search.solutions import SolutionSearch
from f_search.ds.data import DataBestFirst
from abc import abstractmethod


class AStarBase(AlgoSearch):
    """
    ============================================================================
     Base for A* Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSearch,
                 data: DataBestFirst = None,
                 name: str = 'AStarBase') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data,
                         name=name)

    @abstractmethod
    def run(self) -> SolutionSearch:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass     

    def create_cached(self) -> dict[State, int]:
        """
        ========================================================================
         Create the cached dictionary.
        ========================================================================
        """
        data = self._data
        cached: dict[State, int] = dict()
        for state in data.explored:
            cached[state] = data.g[state]
        return cached

    @abstractmethod
    def _create_solution(self, is_valid: bool) -> SolutionSearch:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        pass
    
    @abstractmethod
    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the State's Heuristic-Value.
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
         Explore the Best-StateBase.
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
            if succ not in data.explored:
                self._generate_state(state=succ)

    def _generate_state(self, state: State) -> None:
        """
        ========================================================================
         Generate a new state.
        ========================================================================
        """
        # Aliases
        data = self._data
        stats = self._stats
        # New State (not in Generated)
        if state not in data.generated:
            stats.generated += 1
            self._update_cost(state=state)
            data.generated.push(state=state, cost=data.cost[state])
        # If Best is a better parent for a given State
        elif data.best:
            if data.g[state] > data.g[data.best] + 1:
                self._update_cost(state=state)
                data.generated.push(state=state,
                                    cost=data.cost[state])


    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Search should continue.
        ========================================================================
        """
        return self._data.generated

    def _update_best(self) -> None:
        """
        ========================================================================
         Update the Best-StateBase.
        ========================================================================
        """
        self._data.best = self._data.generated.pop()

    def _update_generated(self) -> None:
        """
        ========================================================================
         Update the Heuristic-Values of States in Generated-List.
        ========================================================================
        """
        data = self._data
        for state in data.generated:
            data.h[state] = self._heuristic(state=state)
            data.cost[state].update(h=data.h[state])
            