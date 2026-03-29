from f_search.algos.i_0_base import AlgoBestFirst
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionOMSPP, SolutionSPP
from f_search.heuristics.phi import UPhi, PhiFunc
from f_search.ds.state import StateBase
from f_search.ds.data.i_2_heuristics_vector import DataHeuristicsVector as Data
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.priority import PriorityGH as Priority
from f_search.stats import StatsSearch
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarAggregative(AlgoOMSPP[State, Data],
                       AlgoBestFirst[ProblemOMSPP, SolutionOMSPP,
                                     State, Data],
                       Generic[State]):
    """
    ============================================================================
     Aggregative A* Algorithm (Eager kA*).
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 phi: PhiFunc = UPhi.min,
                 name: str = 'AStarAggregative',
                 need_path: bool = False,
                 is_analytics: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        frontier = Frontier[State, Priority]()
        self._data = Data(frontier=frontier)
        super().__init__(problem=problem, name=name,
                         is_analytics=is_analytics)
        self._phi = phi
        self._need_path = need_path
        self._all_goals: list[State] = None
        self._active_indices: list[int] = None
        self._prev_explored: int = None
        self._prev_discovered: int = None

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run Pre-Processing.
        ========================================================================
        """
        super()._run_pre()
        self._all_goals = list(self.problem.goals)
        self._active_indices = list(range(len(self._all_goals)))
        self._prev_explored = 0
        self._prev_discovered = 0
        self._prev_heuristic_calcs = 0
        self._explored_offset = 0

    def _run(self) -> SolutionOMSPP:
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
                    break
                continue
            self._explore_best()
        return self._create_solution()

    def _discover(self, state: State) -> None:
        """
        ========================================================================
         Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1
        self._stats.heuristic_calcs += len(self._active_indices)
        # Aliases
        data = self._data
        # Set State's Parent
        data.set_best_to_be_parent_of(state=state)
        # Compute heuristic vector (only for active goals)
        h_vec = [0] * len(self._all_goals)
        for i in self._active_indices:
            h_vec[i] = state.distance(other=self._all_goals[i])
        data.dict_h[state] = h_vec
        # Aggregate for priority
        h_agg = self._phi(h_vec, self._active_indices)
        # Push State to Frontier
        priority = Priority[State](key=state.key,
                                   g=data.dict_g[state],
                                   h=h_agg)
        data.frontier.push(state=state, priority=priority)

    def _on_goal_found(self) -> None:
        """
        ========================================================================
         On Goal Found.
        ========================================================================
        """
        self._collect_explored(goal=self._data.best,
                               algo=self,
                               offset=self._explored_offset)
        self._explored_offset = len(self._data.explored)
        # Remove goal from active sets
        goal = self._data.best
        idx = self._all_goals.index(goal)
        self._goals_active.remove(goal)
        self._active_indices.remove(idx)
        # Append sub-solution
        self._append_sub_solution()
        # Re-aggregate F values for remaining active goals
        if not self._can_terminate():
            self._update_h()
            # Push goal back to frontier for future expansion
            h_agg = self._phi(self._data.dict_h[goal],
                              self._active_indices)
            priority = Priority[State](key=goal.key,
                                       g=self._data.dict_g[goal],
                                       h=h_agg)
            self._data.frontier.push(state=goal,
                                     priority=priority)

    def _append_sub_solution(self) -> None:
        """
        ========================================================================
         Append the Sub-Solution.
        ========================================================================
        """
        problem = ProblemSPP(grid=self.problem.grid,
                             start=self.problem.start,
                             goal=self._data.best)
        stats = StatsSearch(
            explored=self._stats.explored - self._prev_explored,
            discovered=self._stats.discovered - self._prev_discovered,
            heuristic_calcs=(self._stats.heuristic_calcs
                             - self._prev_heuristic_calcs),
            elapsed=self.seconds_since_last_call())
        self._prev_explored = self._stats.explored
        self._prev_discovered = self._stats.discovered
        self._prev_heuristic_calcs = self._stats.heuristic_calcs
        path = None
        if self._need_path:
            path = self._data.path_to(state=self._data.best)
        g_goal = self._data.dict_g[self._data.best]
        solution = SolutionSPP(name_algo=self.name,
                               problem=problem,
                               is_valid=True,
                               path=path,
                               g_goal=g_goal,
                               stats=stats)
        self._sub_solutions.append(solution)

    def _update_h(self) -> None:
        """
        ========================================================================
         Re-aggregate heuristic values for all Frontier states.
        ========================================================================
        """
        for state in self._data.frontier:
            h_vec = self._data.dict_h[state]
            h_agg = self._phi(h_vec, self._active_indices)
            priority = Priority[State](key=state.key,
                                       g=self._data.dict_g[state],
                                       h=h_agg)
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
          lower cost than its current parent.
        ========================================================================
        """
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
        # Recompute aggregated h from stored vector
        h_agg = self._phi(data.dict_h[succ],
                          self._active_indices)
        priority = Priority[State](key=succ.key,
                                   g=data.dict_g[succ],
                                   h=h_agg)
        data.frontier.update(state=succ, priority=priority)
