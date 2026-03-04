from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached
from f_search.problems import ProblemSPP, ProblemOMSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.ds.data import DataCached as Data
from f_search.ds.data import DataCachedAnalytics as DataAnalytics
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarIncrementalBackward(AlgoOMSPP, Generic[State]):
    """
    ========================================================================
     Backward Incremental A* for One-to-Many Shortest-Path-Problem.
    ========================================================================
     Converts OMSPP to MOSPP (Many-to-One) by reversing each sub-problem.
     Runs backward A* from each goal Gi toward the shared original start S.
     Accumulates heuristic info (exact distances and lower bounds toward S)
      across sub-searches. Uses PriorityGHFlags to prefer states with
      cached (exact) heuristics over bounded (lower-bound) over unbounded
      (Manhattan).
    ========================================================================
     depth_propagation controls accumulated heuristic levels:
       -1: cached exact distances only (from optimal path).
        0: cached + lower bounds from explored states.
       >0: cached + lower bounds + BFS propagation at given depth.
    ========================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 depth_propagation: int = 2,
                 name: str = 'AStarIncrementalBackward',
                 need_path: bool = False,
                 is_analytics: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        super().__init__(problem=problem, name=name)
        self._need_path = need_path
        self._depth_propagation = depth_propagation
        self._data_cached = Data[State]()
        self._analytics = DataAnalytics[State]() if is_analytics else None

    @property
    def analytics(self) -> DataAnalytics[State] | None:
        """
        ====================================================================
         Return the Analytics Data (None if is_analytics=False).
        ====================================================================
        """
        return self._analytics

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Run the Algorithm.
        ====================================================================
        """
        # Convert OMSPP to list of forward SPPs
        spps = self.problem.to_spps()
        # Sort: nearest goal to S first (ascending Manhattan)
        start = self.problem.start
        spps.sort(key=lambda p: p.goal.distance(other=start))
        # Run backward A* for each goal
        for i, sub_problem in enumerate(spps):
            is_last = (i == len(spps) - 1)
            reversed_problem = sub_problem.reverse()
            sub_solution = self._run_sub_search(
                forward_problem=sub_problem,
                backward_problem=reversed_problem,
                is_last=is_last)
            if not sub_solution:
                break
            self._sub_solutions.append(sub_solution)
        return self._create_solution()

    def _run_sub_search(self,
                        forward_problem: ProblemSPP,
                        backward_problem: ProblemSPP,
                        is_last: bool = False
                        ) -> SolutionSPP | None:
        """
        ====================================================================
         Run a backward sub-search from Gi to S, extract heuristic info,
          and return a forward SolutionSPP (goal=Gi).
        ====================================================================
        """
        # Run backward A* with flag-aware priorities
        algo = AStarCached[State](
            problem=backward_problem,
            data_cached=self._data_cached,
            need_path=self._need_path)
        backward_solution = algo.run()
        # If no solution found, return None
        if not backward_solution:
            return None
        # Optionally reconstruct forward path
        fwd_path = None
        if self._need_path:
            bwd_path = backward_solution.path
            fwd_path = bwd_path.reverse()
        # Collect analytics (before accumulation mutates _data_cached)
        if self._analytics:
            self._analytics.collect(
                goal_key=forward_problem.goal.key,
                data=algo._data,
                data_cached=self._data_cached)
        # Accumulate heuristic info for future sub-searches
        # (only when goal was reached — early cached termination
        #  has no new path info to extract)
        if not is_last and algo.reached_goal:
            depth = self._depth_propagation
            # Cached exact distances (always collected)
            cached = algo.distances_to_goal()
            self._data_cached.dict_cached.update(cached)
            # Parent pointers for path reconstruction
            path_states = algo._data.path_to(
                state=backward_problem.goal).to_iterable()
            for i in range(len(path_states) - 1):
                self._data_cached.dict_parent[path_states[i]] \
                    = path_states[i + 1]
            # Lower bounds (depth >= 0)
            if depth >= 0:
                bounded = algo.propagate_bounds(depth=depth)
                # Keep the tighter (max) lower bound per state
                for state, value in bounded.items():
                    old = self._data_cached.dict_bounded.get(
                        state)
                    if old is None or value > old:
                        self._data_cached.dict_bounded[state] \
                            = value
        # Return forward sub-solution (problem.goal=Gi for SolutionOMSPP)
        return SolutionSPP(name_algo=self.name,
                           problem=forward_problem,
                           is_valid=True,
                           path=fwd_path,
                           stats=backward_solution.stats)
