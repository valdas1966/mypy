from f_search.algos.i_2_omspp import AlgoOMSPP
from f_search.algos.i_1_spp import AStar
from f_search.problems import ProblemSPP, ProblemOMSPP
from f_search.solutions import SolutionSPP
from f_search.heuristics import HeuristicsProtocol, HeuristicsManhattan as Manhattan
from f_search.ds.data import DataHeuristics as Data
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.priority import PriorityGH as Priority
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarIncremental(AlgoOMSPP[State, Data[State]], Generic[State]):
    """
    ============================================================================
     A* Incremental Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 data: Data[State] = None,
                 heuristics: HeuristicsProtocol[State] = None,
                 name: str = 'AStarIncremental') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._data = data
        if not data:
            frontier = Frontier[State, Priority]()
            self._data = Data[State](frontier=frontier)
        self._heuristics = heuristics
        if not heuristics:
            self._heuristics = Manhattan[State]

    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        # Go through each sub-problem (SPP) in the OMSPP.
        for sub_problem in self.problem.to_spps():
            # If the goal is already explored
            if sub_problem.goal in self._data.explored:
                self._on_goal_already_explored(problem=sub_problem)
                continue
            # Run the sub-search (SPP) using AStar.
            sub_solution = self._run_sub_search(problem=sub_problem)
            if not sub_solution:
                return
            self._sub_solutions.append(sub_solution)
            priority = Priority[State](key=sub_problem.goal.key,
                                       g=self._data.dict_g[sub_problem.goal],
                                       h=self._data.dict_h[sub_problem.goal])
            self._data.frontier.push(state=sub_problem.goal, priority=priority)

    def _on_goal_already_explored(self, problem: ProblemSPP) -> None:
        """
        ========================================================================
         On Goal Already Explored - Append the Sub-Solution.
        ========================================================================
        """
        path = self._data.path_to(state=problem.goal)
        solution = SolutionSPP(problem=problem,
                               is_valid=True,
                               path=path)
        self._sub_solutions.append(solution)

    def _run_sub_search(self, problem: ProblemSPP) -> SolutionSPP:
        """
        ========================================================================
         Run the Sub-Search.
        ========================================================================
        """
        # Update the Heuristics to next goal
        heuristics = self._heuristics(goal=problem.goal)
        # Update states in Frontier with new heuristics
        for state in self._data.frontier:
            # Update each state each time
            self._data.dict_h[state] = heuristics(state)
            priority = Priority[State](key=state.key,
                                       g=self._data.dict_g[state],
                                       h=self._data.dict_h[state])
            self._data.frontier.update(state=state, priority=priority)
        # Run the Sub-Search using AStar.
        algo = AStar[State](problem=problem,
                            data=self._data,
                            heuristics=heuristics)
        return algo.run()