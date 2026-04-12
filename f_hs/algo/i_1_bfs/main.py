from collections import deque
from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFS(Generic[State], AlgoSPP[State]):
    """
    ========================================================================
     Breadth-First Search Algorithm.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'BFS',
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AlgoSPP.__init__(self, problem=problem, name=name,
                         is_recording=is_recording)
        self._open: deque[State] = deque()
        self._open_set: set[State] = set()

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._open.clear()
        self._open_set.clear()
        super()._init_search()

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Append State to the Frontier (FIFO).
        ====================================================================
        """
        self._open.append(state)
        self._open_set.add(state)

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier (FIFO).
        ====================================================================
        """
        state = self._open.popleft()
        self._open_set.discard(state)
        return state

    def _has_open(self) -> bool:
        """
        ====================================================================
         Return True if the Frontier is not empty.
        ====================================================================
        """
        return len(self._open) > 0

    def _in_open(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is in the Frontier.
        ====================================================================
        """
        return state in self._open_set
