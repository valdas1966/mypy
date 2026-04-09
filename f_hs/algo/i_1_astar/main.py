from heapq import heappush, heappop
from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State]):
    """
    ========================================================================
     A* Search Algorithm.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State], float],
                 name: str = 'AStar',
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AlgoSPP.__init__(self, problem=problem, name=name,
                         is_recording=is_recording)
        self._h = h
        self._open: list[tuple[float, float, int, State]] = list()
        self._counter: int = 0

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._open.clear()
        self._counter = 0
        super()._init_search()

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push State into the Priority Queue (by f = g + h).
         Tie-breaking: prefer higher g (deeper), then FIFO.
        ====================================================================
        """
        g = self._g[state]
        f = g + self._h(state)
        self._counter += 1
        heappush(self._open, (f, -g, self._counter, state))

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the State with lowest f-value.
        ====================================================================
        """
        return heappop(self._open)[3]

    def _has_open(self) -> bool:
        """
        ====================================================================
         Return True if the Priority Queue is not empty.
        ====================================================================
        """
        return len(self._open) > 0
