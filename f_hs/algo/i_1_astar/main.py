from f_ds.queues.i_1_indexed import QueueIndexed
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
        self._open: QueueIndexed[State, tuple] = (
            QueueIndexed()
        )

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._open.clear()
        super()._init_search()

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push State into the Priority Queue (by f = g + h).
         Tie-breaking: prefer higher g (deeper node).
        ====================================================================
        """
        g = self._g[state]
        f = g + self._h(state)
        self._open.push(item=state, priority=(f, -g))

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the State with lowest f-value.
        ====================================================================
        """
        return self._open.pop()

    def _has_open(self) -> bool:
        """
        ====================================================================
         Return True if the Priority Queue is not empty.
        ====================================================================
        """
        return bool(self._open)

    def _in_open(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is in the Open List.
        ====================================================================
        """
        return state in self._open

    def _decrease_g(self, state: State) -> None:
        """
        ====================================================================
         Update the Priority of a State in the Open List.
        ====================================================================
        """
        g = self._g[state]
        f = g + self._h(state)
        self._open.decrease_key(item=state,
                                priority=(f, -g))

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Add h and f values to Search Events.
        ====================================================================
        """
        t = event.get('type')
        if t in ('push', 'pop', 'decrease_g'):
            h = self._h(event['state'])
            event['h'] = h
            event['f'] = event['g'] + h
