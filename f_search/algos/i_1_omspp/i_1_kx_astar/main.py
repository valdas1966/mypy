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
        self._sub_problems: list[ProblemOOSPP] = []
        self._sub_solutions: dict[State, SolutionOOSPP] = {}
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
        self._create_sub_problems()
        self._solve_sub_problems()
        return self._create_solution()

    def _create_sub_problems(self) -> None:
        """
        ========================================================================
         Convert ProblemOMSPP into k ProblemOOSPP (one for each goal).
        ========================================================================
        """
        start = self._problem.start
        grid = self._problem.grid
        goals = self._problem.goals

        for goal in goals:
            sub_problem = ProblemOOSPP(grid=grid,
                                       start=start,
                                       goal=goal)
            self._sub_problems.append(sub_problem)

    def _solve_sub_problems(self) -> None:
        """
        ========================================================================
         Execute A* algorithm autonomously for each sub-problem.
        ========================================================================
        """
        for sub_problem in self._sub_problems:
            # Create and run A* for this sub-problem
            astar = AStar(problem=sub_problem, verbose=False)
            solution = astar.run()

            # Store solution indexed by goal
            goal = sub_problem.goal
            self._sub_solutions[goal] = solution

            # Aggregate counters
            if solution.is_valid:
                self._counters['GENERATED'] += solution.stats.generated
                self._counters['UPDATED'] += solution.stats.updated
                self._counters['EXPLORED'] += solution.stats.explored

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
        elapsed_per_goal = {}
        generated_per_goal = {}
        updated_per_goal = {}
        explored_per_goal = {}

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

    def _create_solution(self) -> SolutionOMSPP:
        """
        ========================================================================
         Aggregate all sub-solutions into a single SolutionOMSPP.
        ========================================================================
        """
        self._run_post()

        # Extract paths from all valid sub-solutions
        paths = {}
        all_valid = True

        for goal, solution in self._sub_solutions.items():
            if solution.is_valid:
                paths[goal] = solution.path
            else:
                all_valid = False

        # Solution is valid only if all sub-problems have valid solutions
        is_valid = all_valid and len(paths) == len(self._sub_problems)

        return SolutionOMSPP(is_valid=is_valid,
                            stats=self._stats,
                            paths=paths)
