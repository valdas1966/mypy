from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State]):
    """
    ========================================================================
     A* Search Algorithm — simple, fast path.

     Priority: (f, -g, state). Enrichment: h, f (int). No
     advanced features.

     `search_state` is supported natively (via AlgoSPP) — seeded
     resume and priority auto-refresh live at the base.

     Pro features — HCached cache-hit early termination,
     HBounded pathmax propagation, to_cache harvest, suffix
     stitching — live on `AStarLookup` (i_2_astar_lookup/).
     Passing an HCached or HBounded `h` to simple AStar is a
     **correctness trap** (no early exit, no suffix stitch, no
     admissibility guard) and is rejected with a TypeError.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], int],
                 name: str = 'AStar',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         Rejects HCached / HBounded `h` — those require
         AStarLookup to surface their features safely. Accept
         HCallable and raw callables.
        ====================================================================
        """
        if (type(self) is AStar
                and isinstance(h, (HCached, HBounded))):
            raise TypeError(
                f'{type(h).__name__} requires AStarLookup — '
                'simple AStar lacks early-exit / pathmax / '
                'admissibility-guard support for lookup '
                'heuristics. Use `AStarLookup(..., cache=...)` '
                'or `AStarLookup(..., bounds=...)` instead.')
        AlgoSPP.__init__(self,
                         problem=problem,
                         frontier=FrontierPriority[State](),
                         name=name,
                         is_recording=is_recording,
                         search_state=search_state)
        self._h: HBase[State] = (h if isinstance(h, HBase)
                                 else HCallable[State](fn=h))

    # ──────────────────────────────────────────────────
    #  Priority / Enrichment
    # ──────────────────────────────────────────────────

    def _priority(self, state: State) -> tuple:
        """
        ====================================================================
         Priority = (f, -g, state). Three levels:
           1. f = g + h.
           2. -g — deeper first.
           3. state — deterministic fallback.
        ====================================================================
        """
        g = self._search.g[state]
        f = g + self._h(state)
        return (f, -g, state)

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Add h and f to push / pop / decrease_g events; both
         cast to int (framework's integer-weight assumption).

         No is_cached / is_bounded / propagate handling — those
         live on AStarLookup.
        ====================================================================
        """
        t = event.get('type')
        if t in ('push', 'pop', 'decrease_g'):
            h = int(self._h(event['state']))
            event['h'] = h
            event['f'] = event['g'] + h
