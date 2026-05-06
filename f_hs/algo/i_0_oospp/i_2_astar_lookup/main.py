from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_oospp.i_1_astar.main import AStar
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStarLookup(BPMXMixin, AStar[State], Generic[State]):
    """
    ========================================================================
     A* enhanced by lookup tables and (optional) in-search
     Felner pathmax / BPMX(d).

     Accepts optional `cache`, `bounds`, `rule_bpmx`,
     `depth_bpmx` kwargs; builds the heuristic chain
     internally as
         HCached(base=HBounded(base=HCallable(h)))
     wrapping only the layers the caller actually requested.
     Callers work with plain dicts and never need to know the
     HCached / HBounded / HCallable classes — those are
     implementation details.

     Lookup semantics:
       - `cache: dict[State, CacheEntry]` — perfect h*(state)
         per key. Triggers cache-hit early termination and
         suffix-stitched path reconstruction. Requires `goal`.
       - `bounds: dict[State, int]` — admissible lower bounds
         per state. Max-combined with the base heuristic.
         Unlocks `propagate_pathmax` (pre-search).

     BPMX semantics (composed via `BPMXMixin`):
       - `rule_bpmx ∈ {None, '1', '2', '3', 'CASCADE'}`
         — selects which Felner rule (or cascade) runs at
         each `_pre_expand`. `None` (default) ⇒ mechanism off.
       - `depth_bpmx ∈ {None, int >= 1}` — BFS-subtree depth
         for Rule 1 / 3 / CASCADE; Rule 2 is depth-1 only by
         structural constraint.
       BPMX needs an HBounded layer for storage of lifted
       h-values; when enabled with a callable `h` and no
       explicit `bounds`, an empty bounds dict is auto-wrapped.

     Escape hatch: if `h` is already an `HBase` subclass, it's
     used directly; `cache` / `bounds` must then be None (we
     refuse to silently double-wrap an assembled chain). In
     this case, when BPMX is enabled, the host must supply
     an HBounded somewhere in the chain (constructor verifies).

     `search_state` lives on AlgoSPP — available on every
     AStar-family class, not a Pro feature.
    ========================================================================
    """

    # Factory
    Factory: type = None

    # Per-class scaffold consumed by `BPMXMixin._init_bpmx_mechanism`.
    # Union of pre-search propagate (`cnt_prop_*`) and in-search BPMX
    # (`cnt_bpmx_*`) groups on top of the inherited frontier /
    # search-semantic / memory groups.
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_prop_waves',
         'cnt_prop_attempts',
         'cnt_prop_lifts'),
        ('cnt_bpmx_attempts',
         'cnt_bpmx_successes',
         'cnt_bpmx_depth'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed',
         'mem_cache', 'mem_bounds'),
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
         Build the heuristic chain from the supplied pieces, then
         delegate to AStar.__init__ and initialise BPMX state.

         Validation:
           - `rule_bpmx not in {None, '1', '2', '3', 'CASCADE'}`
             → ValueError.
           - `depth_bpmx not in {None} ∪ {int >= 1}` → ValueError.
           - `rule_bpmx == '2'` with depth_bpmx != 1 → ValueError
             (Rule 2 cannot propagate beyond depth 1).
           - `cache` supplied without `goal` → ValueError.
           - `h` is a pre-built HBase AND `cache`/`bounds` given
             → ValueError (would double-wrap).
           - HCached goal not in problem.goals → ValueError
             (A* admissibility).
           - BPMX enabled but no HBounded reachable in the chain
             → ValueError.

         Auto-wrap: when `rule_bpmx is not None` AND `h` is a
         callable / None AND `bounds` is None, synthesize an
         empty `bounds={}` so the chain builder includes the
         HBounded storage layer.
        ====================================================================
        """
        BPMXMixin._validate_rule_bpmx(rule_bpmx)
        BPMXMixin._validate_depth_bpmx(depth_bpmx)
        BPMXMixin._validate_combination(rule_bpmx=rule_bpmx,
                                        depth_bpmx=depth_bpmx)
        needs_storage = rule_bpmx is not None
        bounds_for_chain = bounds
        if (needs_storage
                and not isinstance(h, HBase)
                and bounds is None):
            bounds_for_chain = {}
        chain = self._build_chain(h=h, cache=cache,
                                  goal=goal, bounds=bounds_for_chain)
        AStar.__init__(self, problem=problem, h=chain, name=name,
                       is_recording=is_recording,
                       search_state=search_state)
        if isinstance(self._h, HCached):
            if self._h.goal not in self.problem.goals:
                raise ValueError(
                    f'HCached goal {self._h.goal!r} is not a goal '
                    f'of the problem; admissibility cannot be '
                    f'guaranteed (cached h* to a different goal '
                    f'may over-estimate h* to the right goal).')
        if (needs_storage
                and BPMXMixin._find_hbounded(self._h) is None):
            raise ValueError(
                'rule_bpmx requires an HBounded in the heuristic '
                'chain as storage for lifted h values; pass `h` '
                'as a callable / None (will auto-wrap) or supply '
                '`bounds=...` (can be empty).')
        self._init_bpmx_mechanism(rule_bpmx=rule_bpmx,
                                  depth_bpmx=depth_bpmx)

    @staticmethod
    def _build_chain(h, cache, goal, bounds) -> HBase:
        """
        ====================================================================
         Assemble the heuristic chain.

         Case A — `h` is a pre-built HBase: use as-is. `cache` /
         `bounds` dicts must be None.

         Case B — `h` is a callable or None: wrap in HCallable
         (h=0 if None), layer HBounded (if `bounds`), then layer
         HCached (if `cache`).
        ====================================================================
        """
        if isinstance(h, HBase):
            if cache is not None or bounds is not None:
                raise ValueError(
                    'cache / bounds cannot be combined with a '
                    'pre-built HBase `h`; pass `h` as a callable '
                    '(or None) and let AStarLookup build the chain.')
            return h
        if cache is not None and goal is None:
            raise ValueError('cache requires a goal.')
        base: HBase = (HCallable(fn=h) if h is not None
                       else HCallable(fn=lambda s: 0))
        chain: HBase = base
        if bounds is not None:
            chain = HBounded(base=chain, bounds=bounds)
        if cache is not None:
            chain = HCached(base=chain, cache=cache, goal=goal)
        return chain

    # ──────────────────────────────────────────────────
    #  Memory Snapshot (extends AlgoSPP's hook)
    # ──────────────────────────────────────────────────

    def _memory_snapshot(self) -> dict[str, int]:
        """
        ====================================================================
         Extends `AlgoSPP._memory_snapshot()` with two
         AStarLookup-specific contributors that walk the
         heuristic chain at end-of-search:

           - `mem_cache`  : HCached `_cache` dict + per-entry
                            CacheEntry overhead + the
                            `h_perfect` float in each entry.
                            (CacheEntry's `suffix_next` is a
                            shared State ref — NOT counted.)
           - `mem_bounds` : HBounded `_bounds` dict + per-value
                            float overhead. (Keys are shared
                            State refs — NOT counted.)

         Reports 0 for layers not present in the chain — e.g.,
         a no-cache run still has `mem_cache=0` so the schema
         stays uniform across all AStarLookup instances.
        ====================================================================
        """
        import sys
        snap = super()._memory_snapshot()
        snap['mem_cache'] = 0
        snap['mem_bounds'] = 0
        cur = self._h
        while cur is not None:
            if isinstance(cur, HCached):
                m = sys.getsizeof(cur._cache)
                for entry in cur._cache.values():
                    m += sys.getsizeof(entry)
                    m += sys.getsizeof(entry.h_perfect)
                snap['mem_cache'] = m
            if isinstance(cur, HBounded):
                m = sys.getsizeof(cur._bounds)
                m += sum(sys.getsizeof(v)
                         for v in cur._bounds.values())
                snap['mem_bounds'] = m
            cur = getattr(cur, '_base', None)
        return snap

    # ──────────────────────────────────────────────────
    #  Priority / Enrichment
    # ──────────────────────────────────────────────────

    def _priority(self, state: State) -> tuple:
        """
        ====================================================================
         Priority = (f, -g, cache_rank, state).
        ====================================================================
        """
        g = self._search.g[state]
        f = g + self._h(state)
        cache_rank = 0 if self._h.is_perfect(state) else 1
        return (f, -g, cache_rank, state)

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Extend AStar's h/f with:
           - `is_cached=True` on push/pop when perfect-h.
           - `is_bounded=True` on push/pop when strictly bounded.
           - int-cast `h` / `h_parent` on propagate events.

         Chains to next `_enrich_event` in MRO via super() —
         BPMXMixin's enrichment (int-casts on
         `pathmax_apply` / `bpmx_lift` / `bpmx_forward`) runs
         first via MRO; this method then layers the lookup
         flags and propagate casts on top.
        ====================================================================
        """
        super()._enrich_event(event)
        t = event.get('type')
        if t in ('push', 'pop'):
            state = event['state']
            if self._h.is_perfect(state):
                event['is_cached'] = True
            if self._h.is_bounded(state):
                event['is_bounded'] = True
        elif t == 'propagate':
            if 'h' in event:
                event['h'] = int(event['h'])
            if 'h_parent' in event:
                event['h_parent'] = int(event['h_parent'])

    # ──────────────────────────────────────────────────
    #  Early-Exit (HCached perfect-h termination)
    # ──────────────────────────────────────────────────

    def _early_exit(self, state: State) -> SolutionSPP | None:
        """
        ====================================================================
         If the heuristic is perfect at `state`, terminate with
         cost = g(state) + h_perfect(state). Only HCached flips
         is_perfect True.
        ====================================================================
        """
        if not self._h.is_perfect(state):
            return None
        h_perfect = self._h(state)
        cost = self._search.g[state] + h_perfect
        self._search.cache_hit = state
        return SolutionSPP(cost=cost)

    # ──────────────────────────────────────────────────
    #  Pre-Search Pathmax Propagation
    # ──────────────────────────────────────────────────

    def propagate_pathmax(self,
                          depth: int | None = None
                          ) -> dict[State, float]:
        """
        ====================================================================
         Pre-search Felner-style pathmax propagation.

         `depth`:
           - `None` (default) — run to convergence (stop when a
             wave tightens nothing; natural termination).
           - `int >= 0` — cap at that many waves.
           - `int < 0` — raises ValueError.

         Requires an HBounded somewhere in the heuristic chain.

         Optimisations:
           - Cached targets skipped (cache is perfect; can't be
             tightened by any lower bound).
           - Last-tightener back-edge skipped (provably useless
             under positive-weight SPP).

         Recording: every (source, child) attempt (except skipped
         back-edges) emits a `propagate` event carrying
         `was_improved: bool`.

         Returns the cumulative dict of states tightened by this
         call, mapped to their final h values.
        ====================================================================
        """
        if depth is not None and depth < 0:
            raise ValueError(
                f'depth must be >= 0 or None; got {depth!r}')
        hb = BPMXMixin._find_hbounded(self._h)
        if hb is None:
            raise ValueError(
                'propagate_pathmax requires an HBounded in the '
                'h chain to store propagated bounds '
                f'(self._h is {type(self._h).__name__}).')
        cached: set[State] = set()
        cur: HBase | None = self._h
        while cur is not None:
            if isinstance(cur, HCached):
                cached.update(cur.cache.keys())
            cur = getattr(cur, '_base', None)
        seeds: set[State] = set(cached) | set(hb.bounds.keys())
        updates: dict[State, float] = {}
        sources: set[State] = seeds
        last_tightener: dict[State, State] = {}
        iteration = 0
        while sources:
            if depth is not None and iteration >= depth:
                break
            # Wave boundary marker — emitted BEFORE this wave's
            # attempts begin; identifies the iteration index so
            # downstream consumers can group subsequent
            # `propagate` events by wave without counting.
            # `num_sources` = source states about to propagate
            # (cheap `len(sources)`); useful for per-wave
            # analytics and early-termination tracking.
            self._counters.inc('cnt_prop_waves')
            self._record_event(type='propagate_wave',
                               depth=iteration,
                               num_sources=len(sources))
            next_sources: set[State] = set()
            for s in sorted(sources):
                h_s = self._h(s)
                skip_back = last_tightener.get(s)
                for n in self.problem.successors(s):
                    if n in cached:
                        continue
                    if skip_back is not None and n == skip_back:
                        continue
                    cand = h_s - self.problem.w(parent=s,
                                                child=n)
                    tightened = hb.add_bound(state=n,
                                             value=cand)
                    new_h = self._h(n)
                    self._counters.inc('cnt_prop_attempts')
                    if tightened:
                        next_sources.add(n)
                        updates[n] = new_h
                        last_tightener[n] = s
                        self._counters.inc('cnt_prop_lifts')
                    self._record_event(
                        type='propagate',
                        state=n,
                        parent=s,
                        h_parent=h_s,
                        h=new_h,
                        was_improved=tightened,
                    )
            sources = next_sources
            iteration += 1
        return updates

    # ──────────────────────────────────────────────────
    #  Cache Harvest
    # ──────────────────────────────────────────────────

    def to_cache(self) -> dict[State, CacheEntry[State]]:
        """
        ====================================================================
         Harvest on-path cache entries from the last completed
         run. Works for both goal-pop and cache-hit termination.
        ====================================================================
        """
        terminated_by_goal = self._search.goal_reached is not None
        terminal: State | None = (self._search.goal_reached
                                  if terminated_by_goal
                                  else self._search.cache_hit)
        if terminal is None:
            raise ValueError(
                'to_cache requires a completed run; no goal '
                'reached and no cache hit.')
        total = self._search.g[terminal]
        if not terminated_by_goal:
            total += self._h(terminal)
        path: list[State] = []
        cur: State | None = terminal
        while cur is not None:
            path.append(cur)
            cur = self._search.parent.get(cur)
        path.reverse()
        out: dict[State, CacheEntry[State]] = {}
        for i, st in enumerate(path):
            if i + 1 < len(path):
                nxt: State | None = path[i + 1]
            elif terminated_by_goal:
                nxt = None
            else:
                nxt = self._h.suffix_next(terminal)
            out[st] = CacheEntry(
                h_perfect=total - self._search.g[st],
                suffix_next=nxt,
            )
        return out

    # ──────────────────────────────────────────────────
    #  Path Reconstruction (suffix-stitching on cache_hit)
    # ──────────────────────────────────────────────────

    def reconstruct_path(self,
                         goal: State | None = None
                         ) -> list[State]:
        """
        ====================================================================
         On cache-hit termination with no explicit `goal`, stitch
         the cached suffix via HCached.suffix_next. Otherwise
         delegate to the base.
        ====================================================================
        """
        if (goal is None
                and self._search.goal_reached is None
                and self._search.cache_hit is not None):
            prefix = AStar.reconstruct_path(
                self, goal=self._search.cache_hit)
            suffix: list[State] = []
            cur = self._h.suffix_next(self._search.cache_hit)
            while cur is not None:
                suffix.append(cur)
                cur = self._h.suffix_next(cur)
            return prefix + suffix
        return AStar.reconstruct_path(self, goal=goal)
