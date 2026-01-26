from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.algos.i_0_base.i_2_astar import AStarBase
from f_search.problems import ProblemSPP, State
from f_search.solutions import SolutionSPP
from f_search.ds.data import DataBestFirst


class AStar(AlgoSPP, AStarBase):
    """
    ============================================================================
     A* Algorithm for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 data: DataBestFirst = None,
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data,
                         name=name)

    def run(self) -> SolutionSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()
        # If incremental algorithm
        if self._data.generated:
            self._update_generated()
        else:
            # If not incremental algorithm
            self._generate_state(state=self._problem.start)
        while self._should_continue():
            self._update_best()
            if self._can_terminate():
                return self._create_solution(is_valid=True)
            self._explore_best()
        return self._create_solution(is_valid=False)        

    def _create_solution(self, is_valid: bool) -> SolutionSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        self._run_post()
        path = self._data.path_to(state=self._data.best) if is_valid else None
        solution = SolutionSPP(is_valid=is_valid,
                               path=path,
                               stats=self._stats)
        return solution

    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the Heuristic-Value of the given State
          (Manhattan-Distance to the Goal).
        ========================================================================
        """
        if state in self.data.cached:
            return self.data.cached[state]
        cell_state = state.key
        cell_goal = self._problem.goal.key
        return cell_state.distance(other=cell_goal)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-StateBase in Generated-List.
        ========================================================================
        """
        return self._data.best == self._problem.goal
