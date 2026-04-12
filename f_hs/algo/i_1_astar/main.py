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
        self._frontier: QueueIndexed[State, tuple] = (
            QueueIndexed()
        )

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.
        ====================================================================
        """
        self._frontier.clear()
        super()._init_search()

    def _frontier_push(self, state: State) -> None:
        """
        ====================================================================
         Push State into the Priority Queue (f = g + h).
         Tie-breaking: prefer higher g (deeper node).
        ====================================================================
        """
        g = self._g[state]
        f = g + self._h(state)
        self._frontier.push(item=state,
                            priority=(f, -g))

    def _frontier_pop(self) -> State:
        """
        ====================================================================
         Pop the State with lowest f-value.
        ====================================================================
        """
        return self._frontier.pop()

    def _has_frontier(self) -> bool:
        """
        ====================================================================
         Return True if the Priority Queue is not empty.
        ====================================================================
        """
        return bool(self._frontier)

    def _in_frontier(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is in the Frontier.
        ====================================================================
        """
        return state in self._frontier

    def _frontier_decrease(self, state: State) -> None:
        """
        ====================================================================
         Update the Priority of a State in the Frontier.
        ====================================================================
        """
        g = self._g[state]
        f = g + self._h(state)
        self._frontier.decrease_key(item=state,
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
