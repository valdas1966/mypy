from f_search.ds import StateBase
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
        self._sub_solutions: dict[StateBase, SolutionSPP] = dict()

    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()        
        self._sub_solutions: dict[StateBase, SolutionSPP] = dict()
        sub_problems: list[ProblemSPP] = self._problem.to_spps()
        n_problems = len(sub_problems)
        for i, sub_problem in enumerate(sub_problems):
            # Run the sub-search.
            name_astar = f'AStar {i+1}/{n_problems}'
            astar = AStar(problem=sub_problem,
                          name=name_astar,
                          verbose=self._verbose)
            solution = astar.run()
            self._sub_solutions[sub_problem.goal] = solution
            # Add stats for the completed goal.
            self._stats.add_goal(goal=sub_problem.goal,
                                 stats=solution.stats)
            if not solution:
                # If any sub-problem is invalid, the overall solution is invalid
                return self._create_solution(is_valid=False)
        # Return valid solution.
        return self._create_solution(is_valid=True)

    def _create_solution(self,
                         is_valid: bool) -> SolutionOMSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        self._run_post()
        return SolutionOMSPP(is_valid=is_valid,
                             stats=self._stats,
                             sub_solutions=self._sub_solutions)
