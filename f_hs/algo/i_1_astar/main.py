from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.frontier.i_1_priority.main import FrontierPriority
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
        AlgoSPP.__init__(self,
                         problem=problem,
                         frontier=FrontierPriority[State](),
                         name=name,
                         is_recording=is_recording)
        self._h = h

    def _priority(self, state: State) -> tuple:
        """
        ====================================================================
         Priority = (f, -g). Prefers lower f, breaks ties
         toward deeper (higher-g) nodes.
        ====================================================================
        """
        g = self._g[state]
        return (g + self._h(state), -g)

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
