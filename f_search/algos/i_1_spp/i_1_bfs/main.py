from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.ds.data import DataBestFirst
from f_search.problems import ProblemSPP
from f_search.ds.frontier import FrontierFifo
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFS(Generic[State], AlgoSPP[State, DataBestFirst[State]]):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 name: str = 'BFS',
                 data: DataBestFirst[State] = None,
                 need_path: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        data = data if data else DataBestFirst(frontier=FrontierFifo())
        super().__init__(problem=problem,
                         data=data,
                         name=name)
        self._need_path = need_path

    def _discover(self, state: State) -> None:
        """
        ========================================================================
         Discover the given State.
        ========================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        # Update the Parent of the State (and its G-Value respectively)
        data.set_best_to_be_parent_of(state=state)
        # Push State to Frontier
        data.frontier.push(state=state)

    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        if succ not in self._data.frontier:
            self._discover(state=succ)
        