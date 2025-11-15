from f_search.ds import State
from f_search.algos import AStar
from f_search.problems import ProblemOMSPP
from f_search.solutions import SolutionOOSPP, SolutionOMSPP
from f_search.algos.i_1_omspp import AlgoOMSPP


class KxAStar(AlgoOMSPP):
    """
    ============================================================================
     K x A* Algorithm for One-to-Many Shortest-Path-Problem.
    ----------------------------------------------------------------------------
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
        self._sub_solutions: dict[State, SolutionOOSPP] = dict()
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
        sub_problems = self._problem.to_oospps()
        for sub_problem in sub_problems:
            astar = AStar(problem=sub_problem)
            self._sub_solutions[sub_problem.goal] = astar.run()
            if not self._sub_solutions[sub_problem.goal]:
                # If any sub-problem is invalid, the overall solution is invalid
                return SolutionOMSPP(is_valid=False,
                                     sub_solutions=self._sub_solutions)        
        return SolutionOMSPP(is_valid=True,
                             sub_solutions=self._sub_solutions)
