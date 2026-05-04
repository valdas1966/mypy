from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_oospp.i_1_astar.main import AStar
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarBPMX(BPMXMixin, AStar[State], Generic[State]):
    """
    ============================================================================
     A* with Felner's Pathmax Rules and BPMX (Bidirectional
     Pathmax) for inconsistent heuristics.

     Composes `BPMXMixin` (in-search mechanism) with vanilla
     `AStar`. Sibling of `AStarLookup`; integrated combination
     with cache/bounds is `AStarLookupBPMX`.

     See `f_hs/algo/oospp/mixins/bpmx/main.py` for the full mechanism
     description (Felner numbering, BPMX(d) cascade, storage,
     frontier-staleness policy, paper references).

     This file is the thin wrapper: validation, heuristic chain
     assembly (callable + optional bounds with auto-wrap),
     mixin initialization. Out of scope (lives on AStarLookup
     / AStarLookupBPMX): HCached early-termination, suffix
     stitching, `to_cache` harvest, pre-search
     `propagate_pathmax`. Pre-built HBase chains containing
     HCached are rejected here — route to AStarLookup.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], int] | None = None,
                 name: str = 'AStarBPMX',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None,
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
           - Pre-built HBase `h` combined with `bounds` →
             ValueError (would double-wrap).
           - Pre-built HBase chain containing HCached →
             TypeError (HCached features belong on AStarLookup).
           - Mechanism enabled but no HBounded reachable →
             ValueError (auto-wraps when `h` is callable / None,
             so this only fires for pre-built chains).

         Auto-wrap: when any mechanism is enabled (rule_pathmax
         or depth_bpmx) AND `h` is callable / None AND `bounds`
         is None, an empty HBounded is auto-wrapped to provide
         storage for lifted h-values.
        ====================================================================
        """
        BPMXMixin._validate_rule_pathmax(rule_pathmax)
        BPMXMixin._validate_depth_bpmx(depth_bpmx)
        if (isinstance(h, HBase)
                and BPMXMixin._chain_contains_hcached(h)):
            raise TypeError(
                'AStarBPMX does not handle HCached chains '
                '(no early-exit / no suffix-stitch). Use '
                'AStarLookup for cache-driven heuristics; or '
                'AStarLookupBPMX for cache + BPMX in one '
                'pass; or pass `h` as a plain callable to '
                'AStarBPMX.')
        bpmx_on = (depth_bpmx is None) or (depth_bpmx > 0)
        pathmax_on = rule_pathmax is not None
        needs_storage = bpmx_on or pathmax_on
        chain = self._build_chain(h=h,
                                  bounds=bounds,
                                  auto_wrap=needs_storage)
        if (needs_storage
                and BPMXMixin._find_hbounded(chain) is None):
            raise ValueError(
                'rule_pathmax / depth_bpmx require an HBounded '
                'in the heuristic chain as storage for lifted '
                'h values; pass `h` as a callable / None (will '
                'auto-wrap) or supply `bounds=...` (can be empty).')
        AStar.__init__(self,
                       problem=problem,
                       h=chain,
                       name=name,
                       is_recording=is_recording,
                       search_state=search_state)
        self._init_bpmx_mechanism(rule_pathmax=rule_pathmax,
                                  depth_bpmx=depth_bpmx)

    # ──────────────────────────────────────────────────
    #  Heuristic Chain Builder
    # ──────────────────────────────────────────────────

    @staticmethod
    def _build_chain(h: HBase | Callable | None,
                     bounds: dict | None,
                     auto_wrap: bool) -> HBase:
        """
        ====================================================================
         Assemble the heuristic chain.

         Pre-built HBase: pass through. `bounds` cannot be
         supplied alongside (would double-wrap).

         Callable / None: wrap in HCallable (h=0 if None),
         then layer HBounded with the supplied bounds dict, or
         with an empty dict when `auto_wrap=True`.
        ====================================================================
        """
        if isinstance(h, HBase):
            if bounds is not None:
                raise ValueError(
                    'bounds cannot be combined with a pre-built '
                    'HBase `h`; pass `h` as a callable.')
            return h
        base: HBase = (HCallable(fn=h) if h is not None
                       else HCallable(fn=lambda s: 0))
        if bounds is not None:
            return HBounded(base=base, bounds=bounds)
        if auto_wrap:
            return HBounded(base=base, bounds={})
        return base
