from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_1_spp import BFS
from f_search.problems import ProblemOMSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.ds.state import StateBase
from f_search.ds.data import DataBestFirst as Data
from f_search.ds.frontier import FrontierFifo as Frontier
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFSIncremental(AlgoOMSPP[State, Data[State]], Generic[State]):
    """
    ============================================================================
     Incremental BFS Algorithm for OMSPP.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 data: Data[State] = None,
                 name: str = 'BFSIncremental') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        frontier = Frontier()
        self._data = data if data else Data(frontier=frontier)
        

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        # Go through each sub-problem (SPP) in the OMSPP.
        for sub_problem in self.problem.to_spps():
            # If the goal is already explored, append the solution.
            if sub_problem.goal in self._data.explored:
                path = self._data.path_to(state=sub_problem.goal)
                solution = SolutionSPP(problem=sub_problem,
                                       is_valid=True,
                                       path=path)
                self._sub_solutions.append(solution)
                continue
            # Run the sub-search (SPP) using BFS.
            algo = BFS(problem=sub_problem,
                       data=self._data)
            sub_solution = algo.run()
            if not sub_solution:
                return
            self._sub_solutions.append(sub_solution)
            self._data.frontier.push(state=sub_problem.goal)

    def _run_post(self) -> None:
        """
        ========================================================================
         Run Post-Processing.
        ========================================================================
        """
        super()._run_post()
        self._output = SolutionOMSPP(problem=self.problem,
                                     subs=self._sub_solutions,
                                     elapsed=self.elapsed)
        
