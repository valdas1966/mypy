from f_search.ds import State
from f_search.algos import AStar
from f_search.ds.data import DataOMSPP
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.algos.i_2_omspp.i_0_base import AlgoOMSPP


class KxAStar(AlgoOMSPP):
    """
    ============================================================================
     K x A* Algorithm for One-to-Many Shortest-Path-Problem.
    ----------------------------------------------------------------------------
     Converts a ProblemOMSPP (One-to-Many) into k-ProblemSPP (One-to-One)
     and executes each autonomously using A* algorithm, then aggregates all
     solutions (paths and stats) into a single SolutionOMSPP.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 data: DataOMSPP = None,
                 verbose: bool = False,
                 name: str = 'KxAStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           data=data,
                           verbose=verbose,
                           name=name)
        self._sub_solutions: dict[State, SolutionSPP] = dict()

    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        # Print the start of the search.
        if self.verbose:
            self._print_start_search()        
        # Initialize the search.
        self._run_pre()        
        # Init Attributes
        self._sub_solutions: dict[State, SolutionSPP] = dict()
        sub_problems: list[ProblemSPP] = self._problem.to_spps()

        for i, sub_problem in enumerate(sub_problems):
            # Print the start of the sub-search.
            if self.verbose:
                self._print_start_sub_search(i=i, sub_problems=sub_problems)
            # Run the sub-search.
            astar = AStar(problem=sub_problem)
            solution = astar.run()
            self._sub_solutions[sub_problem.goal] = solution
            # Add stats for the completed goal.
            self._stats.add_goal(goal=sub_problem.goal,
                                 stats=solution.stats)
            # Print the end of the sub-search.
            if self.verbose:
                self._print_end_sub_search(solution=solution)
            if not solution:
                # If any sub-problem is invalid, the overall solution is invalid
                return self._create_solution(is_valid=False)
        # Create valid solution.
        return self._create_solution(is_valid=True)

    def _create_solution(self,
                         is_valid: bool) -> SolutionOMSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        solution = SolutionOMSPP(is_valid=is_valid,
                                 stats=self._stats,
                                 sub_solutions=self._sub_solutions)
        if self.verbose:
            self._print_end_search()
        return solution

    def _print_start_search(self) -> None:
        """
        ========================================================================
         Print the start of the search.
        ========================================================================
        """
        print(f'[{self.name}] \
                [Start Search] \
                Grid={self._problem.grid}, \
                Start={self._problem.start}, \
                Goals={len(self._problem.goals)}')

    def _print_end_search(self) -> None:
        """
        ========================================================================
         Print the end of the search.
        ========================================================================
        """
        print(f'[{self.name}] \
                [End Search] \
                Generated={self._stats.generated}, \
                Explored={self._stats.explored}, \
                Elapsed={self._stats.elapsed}')

    def _print_start_sub_search(self,
                                i: int,
                                sub_problems: list[ProblemSPP]) -> None:
        """
        ========================================================================
         Print the start of the sub-search.
        ========================================================================
        """
        goal = sub_problems[i].goal
        goals = self._problem.goals
        print(f'[{self.name}] \
                [Start Sub-Search {i+1}/{len(goals)}] \
                Goal={goal}')

    def _print_end_sub_search(self, solution: SolutionSPP) -> None:
        """
        ========================================================================
         Print the end of the sub-search.
        ========================================================================
        """
        print(f'[{self.name}] \
                [End Sub-Search] \
                Path={len(solution.path)}, \
                Generated={solution.stats.generated}, \
                Explored={solution.stats.explored}, \
                Elapsed={solution.stats.elapsed}')
