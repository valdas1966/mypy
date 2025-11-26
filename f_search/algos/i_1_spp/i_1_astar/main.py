from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.problems import ProblemSPP, State
from f_search.solutions import SolutionSPP
from f_search.ds.data import DataSPP
from f_search.ds.cost import Cost
from f_search.ds.path import Path


class AStar(AlgoSPP):
    """
    ============================================================================
     A* Algorithm for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 data: DataSPP = None,
                 verbose: bool = False,
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSPP.__init__(self,
                         problem=problem,
                         data=data,
                         verbose=verbose,
                         name=name)

    def run(self) -> SolutionSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()        
        if not self._data.generated:
            self._generate_state(state=self._problem.start)
        while self._should_continue():
            self._update_best()
            if self._can_terminate():
                return self._create_solution(is_valid=True)
            self._explore_best()
        return self._create_solution(is_valid=False)        

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

    def _create_solution(self, is_valid: bool) -> SolutionSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        # Run post
        self._run_post()
        return SolutionSPP(is_valid=is_valid,
                           data=self._data,
                           stats=self._stats)

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

    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the Heuristic-Value of the given State
          (Manhattan-Distance to the Goal).
        ========================================================================
        """
        cell_state = state.key
        cell_goal = self._problem.goal.key
        return cell_state.distance(other=cell_goal)

    def _update_cost(self, state: State) -> None:
        """
        ========================================================================
         Update the Cost of the given StateBase.
        ========================================================================
        """
        # Aliases
        data = self._data
        data.parent[state] = data.best
        data.g[state] = data.g[data.best] + 1 if data.best else 0
        data.h[state] = self._heuristic(state=state)
        data.cost[state] = Cost(key=state,
                                      g=data.g[state],
                                      h=data.h[state])

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-StateBase in Generated-List.
        ========================================================================
        """
        return self._data.best == self._problem.goal
