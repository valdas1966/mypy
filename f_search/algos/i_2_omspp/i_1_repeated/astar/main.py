from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.algos.i_2_omspp.i_0_base import AlgoOMSPP


class AStarRepeated(AlgoOMSPP):
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
                 name: str = 'KxAStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           name=name)

    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()
        sub_problems: list[ProblemSPP] = self._problem.to_spps()
        n_problems = len(sub_problems)
        for i, sub_problem in enumerate(sub_problems):
            if sub_problem.goal not in self._goals_active:
                continue
            # Run the sub-search.
            name_astar = f'AStar {i+1}/{n_problems}'
            astar = AStar(problem=sub_problem,
                          name=name_astar)
            solution = astar.run()
            self._sub_solutions[sub_problem.goal] = solution
            self._goals_active.remove(sub_problem.goal)
            # Add a solution for the goals that are explored in current A*.
            for goal in self._goals_active:
                if goal in astar._data.explored:
                    path = astar._data.path_to(state=goal)
                    solution = SolutionSPP(is_valid=True, path=path)
                    self._sub_solutions[goal] = solution
                    self._goals_active.remove(goal)
            if not solution:
                # If any sub-problem is invalid, the overall solution is invalid
                break
        # Return solution (valid or invalid)
        return self._create_solution()
