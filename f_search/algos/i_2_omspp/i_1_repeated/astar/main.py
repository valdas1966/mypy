from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.algos.i_2_omspp.i_0_base import AlgoOMSPP
from f_search.stats import StatsSearch as Stats


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
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'KxAStar',
                 need_path: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           name=name)
        self._need_path = need_path

    def _run(self) -> None:
        """
        ========================================================================
         Run the AStarRepeated Algorithm.
        ========================================================================
        """
        sub_problems: list[ProblemSPP] = self.problem.to_spps()
        n_problems = len(sub_problems)
        for i, sub_problem in enumerate(sub_problems):
            if sub_problem.goal not in self._goals_active:
                continue
            # Run the sub-search.
            name_astar = f'AStar {i+1}/{n_problems}'
            astar = AStar(problem=sub_problem,
                          name=name_astar,
                          need_path=self._need_path)
            solution = astar.run()
            if not solution:
                return
            self._goals_active.remove(sub_problem.goal)
            # Add a solution for the goals that are explored in current A*.
            for goal in self._goals_active:
                if goal in astar._data.explored:
                    problem_by_the_way = ProblemSPP(
                        grid=sub_problem.grid,
                        start=sub_problem.start,
                        goal=goal)
                    path = None
                    if self._need_path:
                        path = astar._data.path_to(state=goal)
                    solution_by_the_way = SolutionSPP(
                        name_algo=self.name,
                        problem=problem_by_the_way,
                        is_valid=True,
                        path=path,
                        stats=Stats())
                    self._sub_solutions.append(solution_by_the_way)
                    self._goals_active.remove(goal)
            self._sub_solutions.append(solution)
        
    def _run_post(self) -> None:
        """
        ========================================================================
         Run Post-Processing.
        ========================================================================
        """
        super()._run_post()
        self._output = SolutionOMSPP(name_algo=self.name,
                                     problem=self.problem,
                                     subs=self._sub_solutions,
                                     elapsed=self._elapsed)