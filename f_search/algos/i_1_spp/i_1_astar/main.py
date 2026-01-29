from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.problems import ProblemSPP
from f_search.solutions import SolutionSPP 
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem,
                         make_frontier=FrontierPriority,
                         name=name)

    def run(self) -> SolutionSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._discover(state=self.problem.start)
        while self._should_continue():
            self._select_best()
            if self._can_terminate():
                return self._create_solution()
            self._explore_best()
        return self._create_failure()

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

    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        if succ not in self._data.frontier:
            self._discover(state=succ, parent=self._data.best)
        