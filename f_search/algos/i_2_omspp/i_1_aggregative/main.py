from f_search.problems import State
from f_search.stats import StatsSearch
from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_0_base.i_2_astar import AStarBase
from f_search.problems.i_2_omspp.main import ProblemOMSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP


class AStarAggregative(AlgoOMSPP, AStarBase):
    """
    ============================================================================
    
    ============================================================================
    """
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AStarAggregative') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         name=name)
        self._generated_prev: int = 0
        self._explored_prev: int = 0
        
    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        self._run_pre()
        
        self._generate_state(state=self._problem.start)
        while self._should_continue():
            self._update_best()
            if self._found_goal():
                best = self._data.best
                self._sub_solutions[best] = self._create_sub_sol(is_valid=True)
                self._goals_active.remove(best)
                if self._can_terminate():
                    return self._create_solution()
                self._update_generated()
            self._explore_best()
        goal_invalid = self._goals_active[0]
        self._sub_solutions[goal_invalid] = self._create_sub_sol(is_valid=False)
        return self._create_solution()    
    
    def _run_pre(self) -> None:
        """
        ========================================================================
         Run Pre-Processing.
        ========================================================================
        """
        super()._run_pre()
        self._generated_prev = 0
        self._explored_prev = 0
    
    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the Heuristic-Value of the given State
          (Manhattan-Distance to the Goal).
        ========================================================================
        """
        cell_state = state.key
        cell_goals = [state.key for state in self._goals_active]
        distances = [cell_state.distance(other=cell_goal)
                     for cell_goal in cell_goals]
        return min(distances)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-StateBase in Generated-List.
        ========================================================================
        """
        return not self._goals_active
    
    def _create_sub_sol(self, is_valid: bool) -> SolutionSPP:
        """
        ========================================================================
         Create a Sub-Solution for the given Goal.
        ========================================================================
        """
        elapsed = self.seconds_since_last_call()
        generated = self._stats.generated - self._generated_prev
        explored = self._stats.explored - self._explored_prev
        self._generated_prev = self._stats.generated
        self._explored_prev = self._stats.explored
        stats = StatsSearch(elapsed=elapsed,
                            explored=explored,
                            generated=generated)
        path = self._data.path_to(state=self._data.best) if is_valid else None
        return SolutionSPP(stats=stats, path=path, is_valid=is_valid)

    def _found_goal(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-StateBase in Generated-List.
        ========================================================================
        """
        return self._data.best in self._goals_active
