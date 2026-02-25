from f_search.algos.i_0_base import AlgoBestFirst
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionOMSPP, SolutionSPP
from f_search.heuristics import HeuristicsAggregative
from f_search.ds.state import StateBase
from f_search.ds.data import DataHeuristics as Data
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.priority import PriorityGH as Priority
from f_search.stats import StatsSearch
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarAggregative(AlgoOMSPP[State, Data],
                       AlgoBestFirst[ProblemOMSPP, SolutionOMSPP, State, Data],
                       Generic[State]):
    """
    ============================================================================
     Aggregative A* Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AStarAggregative') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        frontier = Frontier[State, Priority]()
        self._data = Data(frontier=frontier)
        super().__init__(problem=problem, name=name)
        self._heuristics: HeuristicsAggregative[State] = None
        self._prev_explored: int = None
        self._prev_discovered: int = None

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run Pre-Processing.
        ========================================================================
        """
        super()._run_pre()
        self._heuristics = HeuristicsAggregative(self._goals_active)
        self._prev_explored = 0
        self._prev_discovered = 0

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._discover(state=self.problem.start)
        while self._should_continue():
            self._select_best()
            if self._data.best in self._goals_active:
                self._on_goal_found()
            if self._can_terminate():
                return
            self._explore_best()

    def _discover(self, state: State) -> None:
        """
        ========================================================================
            Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        # Set State's Parent
        data.set_best_to_be_parent_of(state=state)
        # Calculate the heuristic distance from state to goal
        data.dict_h[state] = self._heuristics(state=state)
        # Calculate the priority of the State (in the Frontier)
        priority = Priority[State](key=state.key,
                                    g=data.dict_g[state],
                                    h=data.dict_h[state])
        # Push State to Frontier
        data.frontier.push(state=state, priority=priority)

    def _on_goal_found(self) -> None:
        """
        ========================================================================
         On Goal Found.
        ========================================================================
        """
        self._goals_active.remove(self._data.best)
        self._append_sub_solution()
        if not self._can_terminate():
            self._update_h()

    def _append_sub_solution(self) -> None:
        """
        ========================================================================
         Append the Sub-Solution.
        ========================================================================
        """
        problem = ProblemSPP(grid=self.problem.grid,
                             start=self.problem.start,
                             goal=self._data.best)
        stats = StatsSearch(explored=self._stats.explored-self._prev_explored,
                            discovered=self._stats.discovered-self._prev_discovered,
                            elapsed=self.seconds_since_last_call())
        self._prev_explored = self._stats.explored
        self._prev_discovered = self._stats.discovered
        solution = SolutionSPP(name_algo=self.name,
                               problem=problem,
                               is_valid=True,
                               stats=stats)
        self._sub_solutions.append(solution)

    def _update_h(self) -> None:
        """
        ========================================================================
         Update the Heuristics.
        ========================================================================
        """
        # Update states in Frontier with new heuristics
        for state in self._data.frontier:
            # Update each state each time
            self._data.dict_h[state] = self._heuristics(state=state)
            priority = Priority[State](key=state.key,
                                       g=self._data.dict_g[state],
                                       h=self._data.dict_h[state])
            self._data.frontier.update(state=state, priority=priority)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Check if the Algorithm can terminate.
        ========================================================================
        """
        return not self._goals_active

    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        if succ in self._data.frontier:
            if self._need_relax(succ=succ):
                self._relax(succ=succ)
        else:
            self._discover(state=succ)

    def _need_relax(self, succ: State) -> bool:
        """
        ========================================================================
         Return True if through Best-State, the Succ can be reached with a
          lower cost through its current parent.
        ========================================================================
        """
        # Aliases
        g_succ = self._data.dict_g[succ]
        g_best = self._data.dict_g[self._data.best]
        return g_succ > g_best + 1

    def _relax(self, succ: State) -> None:
        """
        ========================================================================
         Relax the Successor.
        ========================================================================
        """
        self._stats.relaxed += 1
        # Aliases
        data = self._data
        # Set the Successor's Parent to the Best-State
        data.set_best_to_be_parent_of(state=succ)
        priority = Priority[State](key=succ.key,
                                   g=data.dict_g[succ],
                                   h=data.dict_h[succ])
        data.frontier.update(state=succ, priority=priority)
