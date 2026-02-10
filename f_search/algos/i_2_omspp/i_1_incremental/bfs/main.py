from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.problems import ProblemOMSPP
from f_search.ds.state import StateBase
from f_search.ds.data import DataBestFirst
from f_search.ds.frontier import FrontierFifo
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFSIncremental(AlgoOMSPP[State, DataBestFirst[State]], Generic[State]):

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'BFSIncremental',
                 data: DataBestFirst[State] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        frontier = FrontierFifo()
        self._data = data if data else DataBestFirst(frontier=frontier)
        super().__init__(problem=problem,
                         data=self._data,
                         name=name)

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        for sub_problem in self.problem.to_spps():
            if sub_problem.goal in self._data.explored:
                continue
            algo = BFS(problem=sub_problem,
                       data=self._data)
            sub_solution = algo.run()
            if not sub_solution:
                return
            self._sub_solutions.append(sub_solution)
            self._data.frontier.push(state=sub_problem.goal)
        

