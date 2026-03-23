from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemOMSPP, ProblemSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.algos.i_2_omspp.i_0_base import AlgoOMSPP


class AStarRepeatedBackward(AlgoOMSPP):
    """
    ========================================================================
     Backward K x A* for One-to-Many Shortest-Path-Problem.
    ========================================================================
     Converts OMSPP to MOSPP (Many-to-One) by reversing each sub-problem.
     Runs backward A* from each goal Gi toward the shared start S.
     No information sharing between sub-searches.
    ========================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AStarRepeatedBackward',
                 need_path: bool = False,
                 is_analytics: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           name=name,
                           is_analytics=is_analytics)
        self._need_path = need_path

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Run the Algorithm.
        ====================================================================
        """
        spps: list[ProblemSPP] = self.problem.to_spps()
        n = len(spps)
        for i, sub_problem in enumerate(spps):
            # Reverse: run from Gi toward S
            reversed_problem = sub_problem.reverse()
            name_astar = f'AStar {i+1}/{n}'
            astar = AStar(problem=reversed_problem,
                          name=name_astar,
                          need_path=self._need_path)
            bwd_solution = astar.run()
            if not bwd_solution:
                break
            self._collect_explored(goal=sub_problem.goal,
                                   algo=astar)
            # Build forward solution
            fwd_path = None
            if self._need_path and bwd_solution.path:
                fwd_path = bwd_solution.path.reverse()
            self._sub_solutions.append(
                SolutionSPP(name_algo=self.name,
                            problem=sub_problem,
                            is_valid=True,
                            path=fwd_path,
                            g_goal=bwd_solution.g_goal,
                            stats=bwd_solution.stats))
        return self._create_solution()
