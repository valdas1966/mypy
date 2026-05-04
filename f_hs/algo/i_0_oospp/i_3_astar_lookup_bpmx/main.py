from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_oospp.i_2_astar_lookup.main import AStarLookup
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarLookupBPMX(BPMXMixin,
                      AStarLookup[State],
                      Generic[State]):
    """
    ============================================================================
     AStarLookup + Felner pathmax / BPMX(d) cascade in one
     pass. The Phase-2 integration class — used by k×A*-CB
     for MOSPP / OMSPP sub-search where cache + bounds +
     in-search BPMX must compose.

     Combines:
       - AStarLookup features (HCached early-termination,
         HBounded admissible bounds, pre-search
         `propagate_pathmax`, suffix-stitched
         `reconstruct_path`, `to_cache` harvest, is_cached /
         is_bounded event flags, 4-tuple priority with
         cache_rank tiebreak).
       - BPMXMixin features (isolated Felner pathmax rules
         {1, 2, 3}, BPMX(d) cascade, 10-counter scaffold,
         pathmax_apply / bpmx_iteration / bpmx_lift /
         bpmx_forward events).

     Constructor mirrors AStarLookup's plus AStarBPMX's two
     mechanism kwargs:
       cache, goal, bounds   ← from AStarLookup.
       rule_pathmax,
         depth_bpmx          ← from BPMXMixin / AStarBPMX.

     Auto-wrap policy (storage for BPMX lifts):
       If a mechanism is enabled (rule_pathmax or BPMX on),
       `h` is a callable / None, and `bounds` is None, we
       synthesize an empty bounds dict so AStarLookup's chain
       builder includes an HBounded layer for storage. With a
       pre-built `HBase` chain, the host is responsible for
       providing HBounded; the constructor verifies and
       raises ValueError otherwise.

     Combined-Class MRO:
         AStarLookupBPMX → BPMXMixin → AStarLookup → AStar
                         → AlgoSPP → ... → object

       - `_pre_expand`        → BPMXMixin (mechanism).
       - `_early_exit`        → AStarLookup (HCached perfect-h).
       - `_priority`          → AStarLookup (4-tuple cache_rank).
       - `reconstruct_path`   → AStarLookup (suffix-stitch on
                                 cache hit).
       - `to_cache`           → AStarLookup.
       - `propagate_pathmax`  → AStarLookup (pre-search waves).
       - `counters`           → BPMXMixin (10-counter scaffold;
                                 frontier-mirrored).
       - `_enrich_event`      → BPMXMixin → AStarLookup → AStar
                                 (chained via super()).

     Out of scope: behavior already on AStarLookup or AStarBPMX.
     This class is a thin orchestrator — its only logic is
     init validation + chain-storage augmentation + mixin init.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], int] | None = None,
                 name: str = 'AStarLookupBPMX',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None,
                 cache: dict[State, CacheEntry[State]] | None = None,
                 goal: State | None = None,
                 bounds: dict[State, float] | None = None,
                 rule_pathmax: int | None = None,
                 depth_bpmx: int | None = 0,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         Validation:
           - `rule_pathmax not in {None, 1, 2, 3}` → ValueError.
           - `depth_bpmx not in {None} ∪ {int >= 0}` →
             ValueError.
           - AStarLookup-side validations (cache without goal;
             pre-built HBase + cache/bounds; HCached goal not
             in problem.goals).
           - Mechanism enabled but no HBounded reachable in
             the resulting chain → ValueError.

         Auto-wrap: when a mechanism is enabled AND `h` is a
         callable / None AND `bounds` is None, synthesize an
         empty `bounds={}` so AStarLookup's chain builder
         includes the HBounded storage layer.
        ====================================================================
        """
        BPMXMixin._validate_rule_pathmax(rule_pathmax)
        BPMXMixin._validate_depth_bpmx(depth_bpmx)
        bpmx_on = (depth_bpmx is None) or (depth_bpmx > 0)
        pathmax_on = rule_pathmax is not None
        needs_storage = bpmx_on or pathmax_on
        bounds_for_lookup = bounds
        if (needs_storage
                and not isinstance(h, HBase)
                and bounds is None):
            bounds_for_lookup = {}
        AStarLookup.__init__(self,
                             problem=problem,
                             h=h,
                             name=name,
                             is_recording=is_recording,
                             search_state=search_state,
                             cache=cache,
                             goal=goal,
                             bounds=bounds_for_lookup)
        if (needs_storage
                and BPMXMixin._find_hbounded(self._h) is None):
            raise ValueError(
                'rule_pathmax / depth_bpmx require an HBounded '
                'in the heuristic chain as storage for lifted '
                'h values; pass `h` as a callable / None (will '
                'auto-wrap) or supply `bounds=...` (can be empty).')
        self._init_bpmx_mechanism(rule_pathmax=rule_pathmax,
                                  depth_bpmx=depth_bpmx)
