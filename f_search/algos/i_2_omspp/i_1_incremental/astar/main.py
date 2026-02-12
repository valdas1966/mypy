from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemOMSPP as Problem
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.heuristics import HeuristicsProtocol, HeuristicsManhattan as Manhattan
from f_search.ds.data import DataHeuristics as Data
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.priority import PriorityGH as Priority
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)

class AStarIncremental(AlgoOMSPP[State, Data[State]], Generic[State]):

    def __init__(self,
                 problem: Problem,
                 data: Data[State] = None,
                 heuristics: HeuristicsProtocol[State] = None,
                 name: str = 'AStarIncremental') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        if not data:
            frontier = Frontier[State, Priority]()
            data = Data[State](frontier=frontier)

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
            # Run the sub-search (SPP) using AStar.
            heuristics = Manhattan[State](goal=sub_problem.goal)
            self._data.update_h(heuristics=heuristics)
            for state in self._data.frontier:
                priority = Priority[State](key=state.key,
                                           g=self._data.dict_g[state],
                                           h=self._data.dict_h[state])
                self._data.frontier.update(state=state, priority=priority)
            algo = AStar[State](problem=sub_problem,
                                data=self._data,
                                heuristics=heuristics)
            sub_solution = algo.run()
            if not sub_solution:
                return
            self._sub_solutions.append(sub_solution)
            self._data.frontier.push(state=sub_problem.goal)
