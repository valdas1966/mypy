from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_astar.main import AStar
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


_VALID_BPMX: frozenset[str | None] = frozenset({
    None, '1', '2', '3',
})


class AStarLookup(Generic[State], AStar[State]):
    """
    ========================================================================
     A* enhanced by lookup tables.

     Accepts optional `cache` and `bounds` dicts; builds the
     heuristic chain internally as
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
         Unlocks `propagate_pathmax`.

     Escape hatch: if `h` is already an `HBase` subclass, it's
     used directly; `cache` / `bounds` must then be None (we
     refuse to silently double-wrap an assembled chain).

     `search_state` lives on AlgoSPP — available on every
     AStar-family class, not a Pro feature.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], int] | None = None,
                 name: str = 'AStar',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None,
                 cache: dict[State, CacheEntry[State]] | None = None,
                 goal: State | None = None,
                 bounds: dict[State, int] | None = None,
                 bpmx: str | None = None,
                 bpmx_depth: int | None = None,
                 ) -> None:
        """
        ====================================================================
         Build the heuristic chain from the supplied pieces, then
         delegate to AStar.__init__.

         Validation:
           - `cache` supplied without `goal` → ValueError.
           - `h` is a pre-built HBase AND `cache`/`bounds` given
             → ValueError (would double-wrap).
           - HCached goal not in problem.goals → ValueError
             (A* admissibility).
           - `bpmx` not in {None, '1', '2', '3'} → ValueError.
             Three distinct behaviours:
               '1' — forward only, tree-deep (Rule 1 sweep).
               '2' — backward only, tree-deep (Rule 2 sweep).
               '3' — full BPMX (Rule 1 + Rule 2, iterated to
                     fixed point) tree-deep.
             Dropped spellings '12', '13', '23', '123' collapse
             into this set: {'13'≡'1', '23'≡'2', '12'≡'3'@tree,
             '123'≡'3'}.
           - `bpmx_depth` not in {None} ∪ {int ≥ 1} → ValueError.
           - `bpmx` enabled but no HBounded reachable in the
             heuristic chain → ValueError (or auto-wrap when
             `h` is a callable / None).

         `bpmx` — in-search pathmax (Felner et al. 2011):
           '1'  — Rule 1, top-down pathmax: propagate h downward
                  through the d-level subtree rooted at the
                  state being expanded. Each ancestor lifts its
                  children via `h(c) ← max(h(c), h(p) − w(p,c))`.
           '2'  — Rule 2, bottom-up pathmax: propagate h upward
                  through the d-level subtree. Each parent lifts
                  itself via `h(p) ← max(h(p), max_c(h(c) −
                  w(c,p)))`.
           '3'  — Full BPMX: iterate Rule 1 top-down + Rule 2
                  bottom-up until a pass tightens nothing.
           None — BPMX off (default).

         `bpmx_depth` — tree depth of the BPMX lookahead subtree
         rooted at the state being expanded (Felner BPMX(d)):
           None (default) — full reachable successor subtree,
                bounded by cycles via the visited-set. Matches
                the framework's use case: `HCached ∘ HBounded ∘
                HCallable` chains may hold inconsistencies at
                any depth below the popped node, so the default
                tightens everywhere inconsistency helps.
                Auto-terminates when a pass tightens nothing.
           1    — flat: only the state and its immediate
                children (the "star" scope); the classical
                Felner BPMX.
           N>1  — BFS `N` levels of successors; rules propagate
                through the full N-level subtree within the
                single expansion.

         BPMX at depth=1 is structurally one-round (Rule 1/Rule 2
         inputs don't feed back into themselves at the same
         level), so '3'@depth=1 behaves identically to a one-
         pass combined Rule 1+Rule 2. The iteration of '3'
         matters only at depth>1 on asymmetric/multi-path
         subgraphs, where a second pass can lift descendants
         that weren't reachable from the root's h until Rule 2
         first lifted intermediate ancestors.

         Irrelevant when `bpmx is None`.
        ====================================================================
        """
        # Validate bpmx string.
        if bpmx not in _VALID_BPMX:
            valid = sorted(v for v in _VALID_BPMX if v is not None)
            raise ValueError(
                f'bpmx must be one of {valid} or None; got '
                f'{bpmx!r}. Under tree-deep BPMX only three '
                f'behaviours are distinct: "1" forward-only, '
                f'"2" backward-only, "3" full-BPMX-iterated. '
                f'Spellings "12"/"13"/"23"/"123" are redundant '
                f'and rejected.')
        # Validate bpmx_depth.
        if bpmx_depth is not None and (not isinstance(bpmx_depth, int)
                                       or bpmx_depth < 1):
            raise ValueError(
                f'bpmx_depth must be int >= 1 or None; got '
                f'{bpmx_depth!r}')
        # Auto-wrap HBounded when BPMX is on and `h` is a
        # callable / None with no explicit bounds.
        if (bpmx is not None
                and bounds is None
                and not isinstance(h, HBase)):
            bounds = {}
        chain = self._build_chain(h=h, cache=cache,
                                  goal=goal, bounds=bounds)
        # BPMX requires HBounded reachable in the chain (for
        # storage). Check after chain is built.
        if bpmx is not None and self._find_hbounded(chain) is None:
            raise ValueError(
                'bpmx requires HBounded in the heuristic chain '
                'as storage for lifted h values. Either pass `h` '
                'as a callable (AStarLookup will auto-wrap) or '
                'supply `bounds=...` (can be empty).')
        self._bpmx: str | None = bpmx
        self._bpmx_depth: int | None = bpmx_depth
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
        ====================================================================
        """
        AStar._enrich_event(self, event)
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
        elif t in ('bpmx_lift', 'bpmx_forward'):
            if 'h_old' in event:
                event['h_old'] = int(event['h_old'])
            if 'h_new' in event:
                event['h_new'] = int(event['h_new'])

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
    #  BPMX — In-Search Pathmax (Rules 1/2/3)
    # ──────────────────────────────────────────────────

    def _pre_expand(self, state: State) -> None:
        """
        ====================================================================
         Tree-deep BPMX (Felner BPMX(d)) at parent expansion.

         Dispatches on `self._bpmx` (string rule selector):
           '1' — Rule 1 top-down sweep over the d-level subtree
                 rooted at `state`.
           '2' — Rule 2 bottom-up sweep over the d-level subtree.
           '3' — Full BPMX: iterate (Rule 2 bottom-up, then
                 Rule 1 top-down) until a pass tightens nothing.
           None — no-op.

         Subtree scope controlled by `self._bpmx_depth` (1 =
         flat; N>1 = N levels; None = full reachable subtree
         bounded by the BFS visited-set).

         Within a pass, Rule 2 runs before Rule 1 (preserves the
         historical flat-depth=1 event order).

         Short-circuits:
           - BPMX off → no-op.
           - `state` is HCached-perfect → skip (no lift possible).
           - No HBounded in chain → enforced at __init__; not
             re-checked here.

         Staleness caveat: Rule 1 mutates descendants' h values
         in HBounded. Descendants already on the frontier from
         earlier expansions carry stale priorities. A* with
         inconsistent heuristics accepts this (Martelli
         construction); Felner's BPMX(d) makes the same choice.
        ====================================================================
        """
        if self._bpmx is None:
            return
        if self._h.is_perfect(state):
            return
        hb = self._find_hbounded(self._h)
        if hb is None:
            return   # defensive; __init__ should have caught.
        levels, edges = self._collect_bpmx_subtree(
            root=state, depth=self._bpmx_depth)
        if self._bpmx == '1':
            self._bpmx_tree_down(levels, edges, hb)
            return
        if self._bpmx == '2':
            self._bpmx_tree_up(levels, edges, hb)
            return
        # '3' — iterate Rule 2 then Rule 1 until fixed point.
        while True:
            changed_up = self._bpmx_tree_up(levels, edges, hb)
            changed_down = self._bpmx_tree_down(levels, edges, hb)
            if not (changed_up or changed_down):
                break

    def _collect_bpmx_subtree(
            self,
            root: State,
            depth: int | None,
            ) -> tuple[list[list[State]], dict[State, list[State]]]:
        """
        ====================================================================
         BFS spanning tree from `root`, up to `depth` levels
         (or full subgraph if depth is None), visited-set
         bounded.

         Returns:
           levels: list of level-lists. levels[k] = states at
                   BFS-depth k. levels[0] = [root].
           edges:  dict mapping each state v in the subtree to
                   its children in the spanning tree (successors
                   of v that were first-visited via v).

         Notes:
           - Spanning tree loses some graph edges when a
             descendant has multiple paths from the root; a
             future DAG-aware variant could recover those. For
             admissibility the spanning tree is sufficient
             (any lift is still a valid lower bound).
           - A cached descendant is still included in the BFS
             (so it can serve as a lift source via Rule 2); the
             per-rule lift methods skip mutating it.
        ====================================================================
        """
        levels: list[list[State]] = [[root]]
        edges: dict[State, list[State]] = {root: []}
        visited: set[State] = {root}
        k = 0
        while True:
            if depth is not None and k >= depth:
                break
            next_level: list[State] = []
            for v in levels[k]:
                for c in self.problem.successors(v):
                    if c in visited:
                        continue
                    visited.add(c)
                    edges[v].append(c)
                    edges.setdefault(c, [])
                    next_level.append(c)
            if not next_level:
                break
            levels.append(next_level)
            k += 1
        return levels, edges

    def _bpmx_tree_down(
            self,
            levels: list[list[State]],
            edges: dict[State, list[State]],
            hb: 'HBounded',
            ) -> bool:
        """
        ====================================================================
         Rule 1 top-down: for k in 0..d-1, lift each level-(k+1)
         child from its level-k ancestor via
         `h(c) ← max(h(c), h(p) − w(p, c))`.
         Cached children skipped (h* can't be improved); closed
         children are NOT skipped — paper-aligned information
         propagation through the expansion subtree regardless
         of closed/open status (admissibility preserved; any
         later re-open under inconsistent-h A* sees the tighter
         h and produces a tighter f).
         Returns True iff any lift fired.
        ====================================================================
        """
        changed = False
        for k in range(len(levels) - 1):
            for p in levels[k]:
                h_p = self._h(p)
                for c in edges[p]:
                    if self._h.is_perfect(c):
                        continue
                    h_c_old = self._h(c)
                    cand = h_p - self.problem.w(parent=p, child=c)
                    if cand > h_c_old:
                        hb.add_bound(state=c, value=cand)
                        self._record_event(
                            type='bpmx_forward',
                            state=c,
                            h_old=h_c_old,
                            h_new=cand,
                            via_parent=p,
                        )
                        changed = True
        return changed

    def _bpmx_tree_up(
            self,
            levels: list[list[State]],
            edges: dict[State, list[State]],
            hb: 'HBounded',
            ) -> bool:
        """
        ====================================================================
         Rule 2 bottom-up: for k in d-1..0, each level-k node
         lifts from its level-(k+1) children via
         `h(p) ← max(h(p), max_c(h(c) − w(c, p)))`.
         Perfect-h parents skipped (cache bound is tighter).
         Returns True iff any lift fired.
        ====================================================================
        """
        changed = False
        for k in range(len(levels) - 2, -1, -1):
            for p in levels[k]:
                children = edges[p]
                if not children:
                    continue
                if self._h.is_perfect(p):
                    continue
                h_p_old = self._h(p)
                best, best_via = h_p_old, None
                for c in children:
                    cand = self._h(c) - self.problem.w(
                        parent=c, child=p)
                    if cand > best:
                        best, best_via = cand, c
                if best > h_p_old:
                    hb.add_bound(state=p, value=best)
                    self._record_event(
                        type='bpmx_lift',
                        state=p,
                        h_old=h_p_old,
                        h_new=best,
                        via_child=best_via,
                    )
                    changed = True
        return changed

    # ──────────────────────────────────────────────────
    #  Pre-Search Pathmax Propagation
    # ──────────────────────────────────────────────────

    @staticmethod
    def _find_hbounded(h: HBase) -> 'HBounded | None':
        """
        ====================================================================
         Walk the `._base` chain; return the first HBounded.
        ====================================================================
        """
        cur: HBase | None = h
        while cur is not None:
            if isinstance(cur, HBounded):
                return cur
            cur = getattr(cur, '_base', None)
        return None

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
        hb = self._find_hbounded(self._h)
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
                    if tightened:
                        next_sources.add(n)
                        updates[n] = new_h
                        last_tightener[n] = s
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
