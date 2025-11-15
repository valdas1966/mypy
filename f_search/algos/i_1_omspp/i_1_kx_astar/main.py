from f_search.algos import AStar, ProblemOOSPP, SolutionOOSPP
from f_search.algos.i_1_omspp import AlgoOMSPP
from f_search.problems import ProblemOMSPP, State
from f_search.solutions import SolutionOMSPP, StatsOMSPP


class KxAStar(AlgoOMSPP):
    """
    ============================================================================
     K x A* Algorithm for One-to-Many Shortest-Path-Problem.

     Converts a ProblemOMSPP (One-to-Many) into k ProblemOOSPP (One-to-One)
     and executes each autonomously using A* algorithm, then aggregates all
     solutions (paths and stats) into a single SolutionOMSPP.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 verbose: bool = False,
                 name: str = 'KxAStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           verbose=verbose,
                           name=name)

    def _run_pre(self) -> None:
        """
        ========================================================================
         Init data structures.
        ========================================================================
        """
        AlgoOMSPP._run_pre(self)
        self._sub_solutions: dict[State, SolutionOOSPP] = dict()
        self._counters['GENERATED'] = 0
        self._counters['UPDATED'] = 0
        self._counters['EXPLORED'] = 0

    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()
        sub_problems = self._problem.to_oospps()
        for sub_problem in sub_problems:
            astar = AStar(problem=sub_problem)
            self._sub_solutions[sub_problem.goal] = astar.run()
            if not self._sub_solutions[sub_problem.goal]:
                # If any sub-problem is invalid, the overall solution is invalid
                break        
        return self._create_solution()

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the end of the Algorithm.
        ========================================================================
        """
        AlgoOMSPP._run_post(self)
        self._stats = self._calc_stats()

    def _calc_stats(self) -> StatsOMSPP:
        """
        ========================================================================
         Calculate aggregate stats from all sub-problems.
        ========================================================================
        """
        # Calculate per-goal stats
        elapsed_per_goal: dict[State, int] = dict()
        generated_per_goal: dict[State, int] = dict()
        updated_per_goal: dict[State, int] = dict()
        explored_per_goal: dict[State, int] = dict()

        for goal, solution in self._sub_solutions.items():
            if solution.is_valid:
                elapsed_per_goal[goal] = solution.stats.elapsed
                generated_per_goal[goal] = solution.stats.generated
                updated_per_goal[goal] = solution.stats.updated
                explored_per_goal[goal] = solution.stats.explored

        return StatsOMSPP(elapsed=self.elapsed,
                          generated=self._counters['GENERATED'],
                          updated=self._counters['UPDATED'],
                          explored=self._counters['EXPLORED'],
                          elapsed_per_goal=elapsed_per_goal,
                          generated_per_goal=generated_per_goal,
                          updated_per_goal=updated_per_goal,
                          explored_per_goal=explored_per_goal)

    def _create_solution(self,
                         sub_solutions: dict[State, SolutionOOSPP]) -> SolutionOMSPP:
        """
        ========================================================================
         Aggregate all sub-solutions into a single SolutionOMSPP.
        ========================================================================
        """
        self._run_post()

        # Solution is valid only if all sub-problems have valid solutions
        is_valid = all(sub_solution.is_valid for sub_solution in sub_solutions.values())

        paths: dict[State, Path] = dict()
        paths = {goal: sub_solution.path for goal, sub_solution in sub_solutions.items()}

        return SolutionOMSPP(is_valid=is_valid,
                            stats=self._stats,
                            paths=paths)
