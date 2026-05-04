from typing import TYPE_CHECKING

from f_core.counters.main import Counters
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_cached.main import HCached

if TYPE_CHECKING:
    pass


class BPMXMixin:
    """
    ============================================================================
     Mixin: Felner pathmax rules + BPMX(d) cascade as a
     reusable in-search mechanism.

     Hosts the search-time pathmax mechanics so multiple AStar
     subclasses can compose them without duplicating code:
       - AStarBPMX (AStar + BPMXMixin) — vanilla A* + BPMX.
       - AStarLookupBPMX (AStarLookup + BPMXMixin) — cache /
         bounds / propagate_pathmax + BPMX in one pass (used
         by k×A*-CB).

     Faithful to Felner et al., "Inconsistent Heuristics in
     Theory and Practice", AIJ 2011.

     Two orthogonal mechanisms (independent kwargs on the host
     class):

       (A) `rule_pathmax ∈ {None, 1, 2, 3}` — isolated Felner
           rule applied once per expansion at the immediate
           parent → children neighborhood (depth 1 only).
           Felner numbering:
             1: parent → child (Mero, 1984):
                  h'(c) = max(h(c), h(p) − w(p, c)).
             2: children → parent via min:
                  h'(p) = max(h(p),
                              min_i(h(c_i) + w(p, c_i))).
             3: single child → parent (reverse pathmax):
                  h'(p) = max(h(p),
                              max_c(h(c) − w(c, p))).

       (B) `depth_bpmx ∈ {0, n ≥ 1, None}` — BPMX(d) cascade
           depth (Felner Algorithm 2). BPMX is the cascading
           combination of Rules 1 + 3 propagated outward
           through the d-level successor subtree of the
           expanded node, iterated to a fixed point. `None`
           propagates through the full reachable subtree
           (visited-set bounded).

     Storage: lifted h-values persist via an `HBounded` layer
     in the heuristic chain. Bounds are admissible by
     construction (triangle inequality), preserving A*
     optimality.

     Frontier staleness: a lift on a state already in the
     frontier with its old priority is left as-is. A* with
     inconsistent heuristics accepts stale priorities (Martelli
     bound; Felner §4 analysis).

     What the mixin expects from the host class:
       - `self._h: HBase` — chain containing an HBounded layer.
       - `self.problem.successors(state)`.
       - `self.problem.w(parent=, child=)`.
       - `self._search.frontier.counters` — frontier owns
         heap-op counters.
       - `self._record_event(...)` — recorder hook.

     The mixin owns:
       - `_pre_expand(state)` override (orchestrates pathmax
         + cascade).
       - `counters` property (10-counter scaffold + frontier
         mirror).
       - `_enrich_event(event)` (int-casts BPMX h_old / h_new;
         chains to next class in MRO via super()).
       - `_init_bpmx_mechanism(rule_pathmax, depth_bpmx)`
         — call from host's __init__ after AStar.__init__.

     MRO contract: place BPMXMixin BEFORE AStar / AlgoSPP in
     the host class's bases so `_pre_expand`, `counters`, and
     `_enrich_event` resolve here first. Example:

         class AStarBPMX(BPMXMixin, AStar[State], Generic[State]):
             ...

         class AStarLookupBPMX(BPMXMixin, AStarLookup[State],
                               Generic[State]):
             ...
    ============================================================================
    """

    _VALID_RULE_PATHMAX: frozenset[int | None] = frozenset(
        {None, 1, 2, 3})

    # 15-name scaffold in 4 visual groups (pathmax 2, bpmx 5,
    # frontier 3 mirrored from FrontierPriority, mem 5 snapshots
    # taken in `_run_post()` AFTER the timer closes).
    # `mem_cache` stays 0 unless an HCached layer is in the
    # chain (only AStarLookupBPMX engages it).
    _BPMX_COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_pathmax_attempts',
         'cnt_pathmax_lifts'),
        ('cnt_bpmx_attempts',
         'cnt_bpmx_iterations',
         'cnt_bpmx_rule3_lifts',
         'cnt_bpmx_rule1_forwards',
         'cnt_bpmx_subtree_states'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('mem_open', 'mem_closed',
         'mem_cache', 'mem_bounds'),
    )

    # ──────────────────────────────────────────────────
    #  Validators (static; for use in host __init__)
    # ──────────────────────────────────────────────────

    @classmethod
    def _validate_rule_pathmax(cls, rule_pathmax: int | None) -> None:
        """
        ====================================================================
         Validate `rule_pathmax` ∈ {None, 1, 2, 3} (Felner
         numbering). Raises ValueError otherwise.
        ====================================================================
        """
        if rule_pathmax not in cls._VALID_RULE_PATHMAX:
            valid = sorted(v for v in cls._VALID_RULE_PATHMAX
                           if v is not None)
            raise ValueError(
                f'rule_pathmax must be one of {valid} or None '
                f'(Felner numbering: 1=parent->child, '
                f'2=children->parent via min, '
                f'3=single child->parent reverse pathmax); '
                f'got {rule_pathmax!r}')

    @staticmethod
    def _validate_depth_bpmx(depth_bpmx: int | None) -> None:
        """
        ====================================================================
         Validate `depth_bpmx` ∈ {None} ∪ {int >= 0}. Rejects
         bool to guard against `depth_bpmx=True` / `False`
         typos. Raises ValueError otherwise.
        ====================================================================
        """
        if depth_bpmx is None:
            return
        if (not isinstance(depth_bpmx, int)
                or isinstance(depth_bpmx, bool)
                or depth_bpmx < 0):
            raise ValueError(
                f'depth_bpmx must be int >= 0 or None; got '
                f'{depth_bpmx!r}')

    # ──────────────────────────────────────────────────
    #  Chain Inspectors (static; chain-walking helpers)
    # ──────────────────────────────────────────────────

    @staticmethod
    def _find_hbounded(h: HBase) -> HBounded | None:
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

    @staticmethod
    def _chain_contains_hcached(h: HBase) -> bool:
        """
        ====================================================================
         True iff the chain has an HCached anywhere.
        ====================================================================
        """
        cur: HBase | None = h
        while cur is not None:
            if isinstance(cur, HCached):
                return True
            cur = getattr(cur, '_base', None)
        return False

    # ──────────────────────────────────────────────────
    #  Initialization (called from host __init__)
    # ──────────────────────────────────────────────────

    def _init_bpmx_mechanism(self,
                             rule_pathmax: int | None,
                             depth_bpmx: int | None) -> None:
        """
        ====================================================================
         Initialize the mechanism state and the 10-counter
         scaffold. Call from the host class's __init__ AFTER
         the AStar.__init__ chain has set `self._h`,
         `self._search`, etc.
        ====================================================================
        """
        self._rule_pathmax: int | None = rule_pathmax
        self._depth_bpmx: int | None = depth_bpmx
        self._counters: Counters = Counters(
            names=self._BPMX_COUNTER_NAMES)

    # ──────────────────────────────────────────────────
    #  Counters property (10-counter scaffold + frontier mirror)
    # ──────────────────────────────────────────────────

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         Live snapshot of the 15-name scaffold. Heap-op counts
         (cnt_push / cnt_pop / cnt_decrease) are the frontier's
         authoritative tally, mirrored on each access via
         `Counters.assign` (single source of truth:
         FrontierPriority). Memory snapshots (mem_*) are
         frozen values populated by `_run_post()` AFTER the
         timer closes.
        ====================================================================
        """
        fc = self._search.frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        self._counters.assign('cnt_decrease', fc['cnt_decrease'])
        for k, v in self._mem.items():
            self._counters.assign(k, v)
        return self._counters

    # ──────────────────────────────────────────────────
    #  Memory Snapshot (extends inherited hook)
    # ──────────────────────────────────────────────────

    def _memory_snapshot(self) -> dict[str, int]:
        """
        ====================================================================
         Extends the inherited `_memory_snapshot()` (AStarLookup
         or AlgoSPP) with the BPMX-specific contributor:

           - `mem_bounds` : HBounded `_bounds` dict + per-value
                            float overhead. (BPMX requires an
                            HBounded layer for storage of
                            lifted h-values.)

         When MRO chains through `AStarLookup._memory_snapshot`
         FIRST (i.e., for `AStarLookupBPMX`), this method's
         `mem_bounds` write idempotently overwrites the same
         value (same HBounded instance — single dict). For
         `AStarBPMX` (no AStarLookup in MRO), this provides
         the ONLY `mem_bounds` source. Either way: schema
         stays consistent.

         Reports 0 if no HBounded is in the chain (defensive;
         BPMXMixin's __init__ guards normally guarantee one
         when a mechanism is enabled).
        ====================================================================
        """
        import sys
        snap = super()._memory_snapshot()
        snap.setdefault('mem_cache', 0)
        snap.setdefault('mem_bounds', 0)
        hb = self._find_hbounded(self._h)
        if hb is not None:
            m = sys.getsizeof(hb._bounds)
            m += sum(sys.getsizeof(v)
                     for v in hb._bounds.values())
            snap['mem_bounds'] = m
        return snap

    # ──────────────────────────────────────────────────
    #  Event Enrichment (chains to next class in MRO)
    # ──────────────────────────────────────────────────

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Add int-cast for `h_old` / `h_new` on pathmax / BPMX
         events. Chains to next `_enrich_event` in MRO via
         super() — for AStarBPMX that's AStar (h, f); for
         AStarLookupBPMX that's AStarLookup (is_cached,
         is_bounded, propagate casts) → AStar (h, f).
        ====================================================================
        """
        super()._enrich_event(event)
        t = event.get('type')
        if t in ('pathmax_apply', 'bpmx_lift', 'bpmx_forward'):
            for k in ('h_old', 'h_new'):
                if k in event:
                    event[k] = int(event[k])

    # ──────────────────────────────────────────────────
    #  Pre-Expand Hook (drives the mechanism)
    # ──────────────────────────────────────────────────

    def _pre_expand(self, state) -> None:
        """
        ====================================================================
         Apply the isolated pathmax rule (if enabled) at depth
         1 around `state`, then run the BPMX(d) cascade (if
         enabled) over the d-level subtree rooted at `state`.

         Order: isolated rule first (cheap, depth-1 only);
         BPMX cascade second (may extend deeper). Both share
         the HBounded storage; the cascade sees any lifts the
         isolated rule produced and may extend them outward.
        ====================================================================
        """
        if self._rule_pathmax is not None:
            self._apply_pathmax(state=state)
        if self._depth_bpmx is None or self._depth_bpmx > 0:
            self._apply_bpmx(state=state)

    # ──────────────────────────────────────────────────
    #  Isolated Pathmax (depth-1 only)
    # ──────────────────────────────────────────────────

    def _apply_pathmax(self, state) -> None:
        """
        ====================================================================
         Apply `rule_pathmax` once at the immediate parent →
         children neighborhood. No cascading.
        ====================================================================
        """
        rule = self._rule_pathmax
        self._counters.inc('cnt_pathmax_attempts')
        hb = self._find_hbounded(self._h)
        if hb is None:
            return
        children = list(self.problem.successors(state))
        if not children:
            return
        if rule == 1:
            self._pathmax_rule1(state=state, children=children, hb=hb)
        elif rule == 2:
            self._pathmax_rule2(state=state, children=children, hb=hb)
        elif rule == 3:
            self._pathmax_rule3(state=state, children=children, hb=hb)

    def _pathmax_rule1(self,
                       state,
                       children: list,
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 1 (Mero, 1984): parent → child.
             h'(c) = max(h(c), h(p) − w(p, c)).
         Lifts each child's h from the popped parent's h.
        ====================================================================
        """
        h_p = self._h(state)
        for c in children:
            if self._h.is_perfect(c):
                continue
            h_c_old = self._h(c)
            cand = h_p - self.problem.w(parent=state, child=c)
            if cand > h_c_old:
                hb.add_bound(state=c, value=cand)
                self._counters.inc('cnt_pathmax_lifts')
                self._record_event(
                    type='pathmax_apply',
                    state=c,
                    rule=1,
                    h_old=h_c_old,
                    h_new=cand,
                    via_parent=state,
                )

    def _pathmax_rule2(self,
                       state,
                       children: list,
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 2 (Felner): children → parent via min.
             h'(p) = max(h(p), min_i(h(c_i) + w(p, c_i))).
         The parent's h is bounded by the cheapest child path.
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        h_p_old = self._h(state)
        cand = min(self._h(c) + self.problem.w(parent=state, child=c)
                   for c in children)
        if cand > h_p_old:
            hb.add_bound(state=state, value=cand)
            self._counters.inc('cnt_pathmax_lifts')
            self._record_event(
                type='pathmax_apply',
                state=state,
                rule=2,
                h_old=h_p_old,
                h_new=cand,
                via_children=tuple(children),
            )

    def _pathmax_rule3(self,
                       state,
                       children: list,
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 3 (Felner): single child → parent (reverse pathmax).
             h'(p) = max(h(p), max_c(h(c) − w(c, p))).
         The parent's h is bounded from below by the strongest
         child's reverse-pathmax estimate.
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        h_p_old = self._h(state)
        best, best_via = h_p_old, None
        for c in children:
            cand = self._h(c) - self.problem.w(parent=c, child=state)
            if cand > best:
                best, best_via = cand, c
        if best > h_p_old:
            hb.add_bound(state=state, value=best)
            self._counters.inc('cnt_pathmax_lifts')
            self._record_event(
                type='pathmax_apply',
                state=state,
                rule=3,
                h_old=h_p_old,
                h_new=best,
                via_child=best_via,
            )

    # ──────────────────────────────────────────────────
    #  BPMX(d) Cascade (Rules 1 + 3, iterated)
    # ──────────────────────────────────────────────────

    def _apply_bpmx(self, state) -> None:
        """
        ====================================================================
         Felner Algorithm 2: BPMX(d) cascade.

         BFS-spans the d-level successor subtree from `state`,
         then iterates (Rule 3 bottom-up, Rule 1 top-down)
         until no pass tightens any node. `state` itself is
         the BFS root; cached descendants (perfect-h) are
         skipped from lift mutation.

         `depth = None` propagates through the full reachable
         subtree (visited-set bounded). Self-amortizes via
         the no-improvement short-circuit.
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        hb = self._find_hbounded(self._h)
        if hb is None:
            return
        levels, edges = self._collect_bpmx_subtree(
            root=state, depth=self._depth_bpmx)
        n_states = sum(len(L) for L in levels)
        self._counters.inc('cnt_bpmx_attempts')
        self._counters.inc('cnt_bpmx_subtree_states', n=n_states)
        iteration = 0
        while True:
            iteration += 1
            self._counters.inc('cnt_bpmx_iterations')
            self._record_event(
                type='bpmx_iteration',
                state=state,
                iteration=iteration,
                num_levels=len(levels),
                num_states=n_states,
            )
            up_changed = self._bpmx_rule3_up(levels, edges, hb)
            down_changed = self._bpmx_rule1_down(levels, edges, hb)
            if not (up_changed or down_changed):
                break

    def _bpmx_rule3_up(self,
                       levels: list[list],
                       edges: dict,
                       hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 3 (single child → parent) sweep, bottom-up over
         the BFS subtree. For each level k from d−1 down to 0,
         each parent at level k lifts from its strongest child
         at level k+1.

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
                    self._counters.inc('cnt_bpmx_rule3_lifts')
                    self._record_event(
                        type='bpmx_lift',
                        state=p,
                        h_old=h_p_old,
                        h_new=best,
                        via_child=best_via,
                    )
                    changed = True
        return changed

    def _bpmx_rule1_down(self,
                         levels: list[list],
                         edges: dict,
                         hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 1 (parent → child) sweep, top-down over the BFS
         subtree. For each level k from 0 to d−1, each parent
         lifts every child at level k+1.

         Cached children skipped (h* cannot be tightened).
         Closed children NOT skipped: paper-aligned —
         admissibility is preserved and a re-open under
         inconsistent-h A* benefits from the tighter h.

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
                        self._counters.inc(
                            'cnt_bpmx_rule1_forwards')
                        self._record_event(
                            type='bpmx_forward',
                            state=c,
                            h_old=h_c_old,
                            h_new=cand,
                            via_parent=p,
                        )
                        changed = True
        return changed

    def _collect_bpmx_subtree(
            self,
            root,
            depth: int | None,
            ) -> tuple[list[list], dict]:
        """
        ====================================================================
         BFS spanning tree from `root` up to `depth` levels (or
         the full reachable subgraph when `depth is None`),
         visited-set bounded.

         Returns:
           levels: levels[k] = states at BFS depth k.
                   levels[0] = [root].
           edges:  state → list of children in the spanning
                   tree (successors first-visited via that
                   state).

         The spanning tree loses graph edges where a descendant
         has multiple paths from the root. For admissibility
         this is fine — any lift derived from the spanning tree
         is a valid lower bound. A DAG-aware variant
         (multi-parent edges) is a future optimisation.
        ====================================================================
        """
        levels: list[list] = [[root]]
        edges: dict = {root: []}
        visited: set = {root}
        k = 0
        while True:
            if depth is not None and k >= depth:
                break
            next_level: list = []
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
