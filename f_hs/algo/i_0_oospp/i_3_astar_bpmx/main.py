from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_oospp.i_2_astar_lookup.main import AStarLookup
from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarBPMX(BPMXMixin, AStarLookup[State], Generic[State]):
    """
    ========================================================================
     AStarLookup + in-search Felner pathmax / BPMX(d).

     Extends AStarLookup with the BPMXMixin's per-expansion
     pathmax dispatch (Rules 1, 2, 3, CASCADE). All cache,
     bounds, propagate_pathmax, and to_cache machinery is
     inherited unchanged from AStarLookup.

     BPMX semantics (composed via `BPMXMixin`):
       - `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}` —
         selects which Felner rule (or cascade) runs at each
         `_pre_expand`. `None` (default) ⇒ mechanism off
         (degenerate case identical to AStarLookup).
       - `depth_bpmx ∈ {None, int >= 1}` — BFS-subtree depth
         for Rule 1 / 3 / CASCADE; Rule 2 is depth-1 only by
         structural constraint.

     BPMX requires an `HBounded` storage layer in the
     heuristic chain (lifted h-values are written there). The
     constructor auto-wraps an empty `bounds={}` when
     `rule_bpmx is not None` AND `h` is a callable / None AND
     no explicit `bounds` was supplied. With a pre-built
     `HBase` chain the host must already include `HBounded`
     (constructor verifies; otherwise ValueError).

     MRO: AStarBPMX → BPMXMixin → AStarLookup → AStar →
     AlgoSPP. The mixin sits between AStarBPMX and AStarLookup
     so its `_pre_expand`, `counters`, and `_enrich_event`
     overrides resolve before AStarLookup's.
    ========================================================================
    """

    # Factory
    Factory: type = None

    # Per-class scaffold consumed by both `AStarLookup.__init__`
    # (replaces inherited 8-name AlgoSPP scaffold) and
    # `BPMXMixin._init_bpmx_mechanism` (rebuilds with the same
    # 16 names — propagate 3 + bpmx 3 + frontier 3 + search 2 +
    # memory 5 incl. mem_total).
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_prop_waves',
         'cnt_prop_attempts',
         'cnt_prop_lifts'),
        ('cnt_bpmx_attempts',
         'cnt_bpmx_lifts',
         'cnt_bpmx_depth'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed',
         'mem_cache', 'mem_bounds', 'mem_total'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], int] | None = None,
                 name: str = 'AStar',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None,
                 cache: dict[State, CacheEntry[State]] | None = None,
                 goal: State | None = None,
                 bounds: dict[State, int] | None = None,
                 rule_bpmx: str | None = None,
                 depth_bpmx: int | None = 1,
                 ) -> None:
        """
        ====================================================================
         Validate BPMX kwargs, auto-wrap empty `bounds={}` for
         BPMX storage when needed, delegate the cache / bounds /
         chain-assembly work to `AStarLookup.__init__`, then
         initialise BPMX mechanism state.

         Validation:
           - `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}`
             → ValueError.
           - `depth_bpmx not in {None} ∪ {int >= 1}` → ValueError.
           - `rule_bpmx == '2'` with `depth_bpmx != 1` →
             ValueError (Rule 2 cannot propagate beyond depth 1).
           - `rule_bpmx is not None` but no HBounded reachable
             in the heuristic chain → ValueError.

         Auto-wrap: when `rule_bpmx is not None` AND `h` is a
         callable / None AND `bounds` is None, synthesise an
         empty `bounds={}` so AStarLookup's chain builder
         includes the HBounded storage layer.
        ====================================================================
        """
        BPMXMixin._validate_rule_bpmx(rule_bpmx)
        BPMXMixin._validate_depth_bpmx(depth_bpmx)
        BPMXMixin._validate_combination(rule_bpmx=rule_bpmx,
                                        depth_bpmx=depth_bpmx)
        bounds_for_chain = bounds
        if (rule_bpmx is not None
                and not isinstance(h, HBase)
                and bounds is None):
            bounds_for_chain = {}
        AStarLookup.__init__(
            self,
            problem=problem,
            h=h,
            name=name,
            is_recording=is_recording,
            search_state=search_state,
            cache=cache,
            goal=goal,
            bounds=bounds_for_chain,
        )
        if (rule_bpmx is not None
                and BPMXMixin._find_hbounded(self._h) is None):
            raise ValueError(
                'rule_bpmx requires an HBounded in the heuristic '
                'chain as storage for lifted h values; pass `h` '
                'as a callable / None (will auto-wrap) or supply '
                '`bounds=...` (can be empty).')
        self._init_bpmx_mechanism(rule_bpmx=rule_bpmx,
                                  depth_bpmx=depth_bpmx)
