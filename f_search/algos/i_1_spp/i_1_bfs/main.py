from f_search.algos.i_0_base.i_1_best_first import AlgoBestFirst
from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.problems import ProblemSPP as Problem
from f_search.solutions import SolutionSPP as Solution
from f_search.ds.data import DataBestFirst as Data
from f_search.ds.state import StateBase as State
from f_search.ds.frontier import FrontierFifo


class BFS(AlgoSPP[Data], AlgoBestFirst[Data]):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: Problem,
                 data: Data = None,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         data=data, name=name,
                         type_frontier=FrontierFifo)

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._discover(state=self._problem.start)
        while self._should_continue():
            self._update_best()
            if self._can_terminate():
                return self._create_solution(is_valid=True)
            self._explore_best()
        return self._create_solution(is_valid=False)

    def _discover(self, state: State, parent: State = None) -> None:
        """
        ========================================================================
         Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        # Set State's Parent
        data.dict_parent[state] = parent
        # Set State's G-Value (based on Parent g-value if exists, otherwise 0)
        data.dict_g[state] = data.dict_g[parent] + 1 if parent else 0
        # Push State to Frontier
        data.frontier.push(state=state)

    def _need_relax(self, state: State) -> bool:
        """
        ========================================================================
         BFS does not need to relax states.
        ========================================================================
        """
        return False
