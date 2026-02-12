from f_search.algos.i_1_neighborhood._bfs_modified import BFSModified
from f_search.algos.i_0_base import AlgoSearch
from f_search.problems import ProblemSPP, ProblemNeighborhood as Problem
from f_search.solutions import SolutionNeighborhood as Solution
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)

class BFSNeighborhood(AlgoSearch[Problem, Solution], Generic[State]):
    """
    ============================================================================
     BFS Neighborhood Algorithm.
    ============================================================================
    """
    
    # Factory
    Factory: type | None = None

    def __init__(self,
                 problem: Problem,
                 name: str = 'BFSNeighborhood') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._neighborhood: dict[State] | None = None
        
    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        problem_spp = ProblemSPP.Factory.fictive_goal(grid=self.problem.grid,
                                                      start=self.problem.start)
        bfs = BFSModified[State](problem=problem_spp,
                                 steps_max=self.problem.steps_max)
        bfs.run()
        self._neighborhood = bfs._data.explored

    def _run_post(self) -> None:
        """
        ========================================================================
         Run the Post-Execution.
        ========================================================================
        """
        super()._run_post()
        self._output = Solution(problem=self.problem,
                                neighborhood=self._neighborhood,
                                stats=self._stats)
