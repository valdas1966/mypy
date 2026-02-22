from f_search.algos.i_1_spp.i_0_base import AlgoSPP
from f_search.ds.data import DataBestFirst as Data
from f_search.ds.priority import PriorityG as Priority
from f_search.problems import ProblemSPP
from f_search.ds.frontier import FrontierPriority as Frontier
from f_search.ds.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class Dijkstra(Generic[State], AlgoSPP[State, Data[State]]):
    """
    ============================================================================
     Dijkstra's Algorithm.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP,
                 name: str = 'Dijkstra',
                 data: Data[State] = None,
                 need_path: bool = True) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        data = data if data else Data(frontier=Frontier())
        super().__init__(problem=problem,
                         data=data,
                         name=name,
                         need_path=need_path)

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
        priority = Priority(key=state.key, g=data.dict_g[state])
        data.frontier.push(state=state, priority=priority)

    def _handle_successor(self, succ: State) -> None:
        """
        ========================================================================
         Handle the Successor.
        ========================================================================
        """
        if succ not in self._data.frontier:
            self._discover(state=succ)
        