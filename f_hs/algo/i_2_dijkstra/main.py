from f_hs.algo.i_1_astar.main import AStar
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class Dijkstra(Generic[State], AStar[State]):
    """
    ========================================================================
     Dijkstra's Algorithm (A* with h=0).
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'Dijkstra',
                 is_recording: bool = False) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AStar.__init__(self, problem=problem,
                       h=lambda s: 0.0, name=name,
                       is_recording=is_recording)

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         No-op override of AStar's h/f enrichment. For Dijkstra,
         h is constant (0) and f equals g — both violate the
         framework Recording Principle (no constants, no derivable
         fields). Dropping them makes Dijkstra events schema-match
         BFS events.
        ====================================================================
        """
        pass
