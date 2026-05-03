from f_core.counters.main import Counters
from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_astar.main import AStar
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


_VALID_RULE_PATHMAX: frozenset[int | None] = frozenset({None, 1, 2, 3})


class AStarBPMX(Generic[State], AStar[State]):
    """
    ============================================================================
     A* with Felner's Pathmax Rules and BPMX (Bidirectional
     Pathmax) for inconsistent heuristics.

     Two orthogonal mechanisms, both grounded in Felner et~al.,
     "Inconsistent Heuristics in Theory and Practice", AIJ 2011:

       (A) `rule_pathmax` -- one of Felner's three pathmax rules,
           applied once per expansion across the immediate
           parent->children neighborhood (depth = 1 only):

             1: Rule 1 (Mero, 1984) -- parent->child:
                  h'(c) = max(h(c), h(p) - w(p, c)).
             2: Rule 2 (Felner) -- children->parent via min:
                  h'(p) = max(h(p),
                              min_i(h(c_i) + w(p, c_i))).
             3: Rule 3 (Felner) -- single child->parent
                (reverse pathmax):
                  h'(p) = max(h(p),
                              max_c(h(c) - w(c, p))).
             None: no isolated pathmax rule.

       (B) `depth_bpmx` -- BPMX(d) cascade depth (Felner
           Algorithm 2). BPMX is the cascading combination of
           Rules 1 + 3 propagated outward through the d-level
           successor subtree of the expanded node, iterated to
           a fixed point:

             0:           BPMX off (default).
             n >= 1:      cascade up to n levels deep.
             None:        cascade through the full reachable
                          subtree; visited-set bounded; stops
                          when no improvement.

     Both knobs are independent. With both on, the isolated
     pathmax rule fires once at the immediate level and the
     BPMX cascade additionally propagates Rules 1 + 3 outward.
     If `rule_pathmax in {1, 3}` and BPMX is on, the chosen
     rule fires twice within one expansion -- redundant but
     correct (BPMX is idempotent; the second pass tightens
     nothing).

     Storage: lifted h-values persist via an `HBounded` layer
     in the heuristic chain. Auto-wraps an empty `HBounded`
     when `bounds=None` AND `h` is a callable AND a mechanism
     is enabled. Bounds are admissible by construction
     (triangle inequality), so A*'s optimality is preserved.

     Frontier staleness: lifted h on a state already on the
     frontier with its old priority is left as-is. A* with
     inconsistent heuristics accepts stale priorities (Martelli
     bound; Felner Section 4 analysis). Re-heaping is not done.

     Counters (3-group scaffold; 10 names total):
       pathmax (2):
         cnt_pathmax_attempts    -- expansions where a
                                    rule_pathmax pass ran.
         cnt_pathmax_lifts       -- successful tightenings.
       bpmx (5):
         cnt_bpmx_attempts       -- expansions where a BPMX
                                    cascade was triggered.
         cnt_bpmx_iterations     -- total iteration rounds
                                    summed across all BPMX
                                    cascades.
         cnt_bpmx_rule3_lifts    -- Rule 3 fires (parent up).
         cnt_bpmx_rule1_forwards -- Rule 1 fires (child down).
         cnt_bpmx_subtree_states -- total states visited during
                                    BPMX subtree BFS.
       frontier (3, mirrored from FrontierPriority):
         cnt_push, cnt_pop, cnt_decrease.

     Recording event types (in addition to AStar's
     push / pop / decrease_g):

       pathmax_apply  -- isolated rule_pathmax fire.
                         {state, rule, h_old, h_new,
                          via_parent? | via_child? | via_children?}.
       bpmx_iteration -- BPMX cascade round-marker (state-tagged
                         to the popped node).
                         {state, iteration, num_levels,
                          num_states}.
       bpmx_lift      -- Rule 3 fired during BPMX (parent up).
                         {state, h_old, h_new, via_child}.
       bpmx_forward   -- Rule 1 fired during BPMX (child down).
                         {state, h_old, h_new, via_parent}.

     `h_old` and `h_new` are int-cast on enrichment for
     consistency with AStar's push/pop/decrease_g schema.

     Out of scope (deferred to a Phase-2 integration class):
       - HCached early-termination, suffix-stitching,
         to_cache harvest -- live on AStarLookup.
       - Pre-search `propagate_pathmax` from cached seeds --
         lives on AStarLookup. AStarBPMX runs only the
         in-search Felner rules.

     If a pre-built HBase chain containing HCached is passed,
     AStarBPMX raises -- HCached features (early-exit,
     suffix-stitch) are AStarLookup territory; mixing here
     would silently drop them.
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
           - `rule_pathmax not in {None, 1, 2, 3}` -> ValueError.
           - `depth_bpmx not in {None} ∪ {int >= 0}` -> ValueError.
           - Pre-built HBase `h` combined with `bounds` -> ValueError
             (would double-wrap).
           - Pre-built HBase chain containing HCached -> ValueError
             (HCached features belong on AStarLookup).
           - Mechanism enabled but no HBounded reachable in the
             chain -> ValueError (auto-wraps when `h` is a
             callable / None, so this only fires for pre-built
             chains).

         Auto-wrap: when any mechanism is enabled (rule_pathmax
         or depth_bpmx) AND `h` is callable / None AND `bounds`
         is None, an empty HBounded is auto-wrapped to provide
         storage for lifted h-values.
        ====================================================================
        """
        # Validate rule_pathmax (None or 1 / 2 / 3 in Felner numbering).
        if rule_pathmax not in _VALID_RULE_PATHMAX:
            valid = sorted(v for v in _VALID_RULE_PATHMAX
                           if v is not None)
            raise ValueError(
                f'rule_pathmax must be one of {valid} or None '
                f'(Felner numbering: 1=parent->child, '
                f'2=children->parent via min, '
                f'3=single child->parent reverse pathmax); '
                f'got {rule_pathmax!r}')
        # Validate depth_bpmx.
        if depth_bpmx is not None and (
                not isinstance(depth_bpmx, int)
                or isinstance(depth_bpmx, bool)
                or depth_bpmx < 0):
            raise ValueError(
                f'depth_bpmx must be int >= 0 or None; got '
                f'{depth_bpmx!r}')
        # Reject HCached chains (out of scope; route to AStarLookup).
        if isinstance(h, HBase) and self._chain_contains_hcached(h):
            raise TypeError(
                'AStarBPMX does not handle HCached chains '
                '(no early-exit / no suffix-stitch). Use '
                'AStarLookup for cache-driven heuristics; or '
                'pass `h` as a plain callable to AStarBPMX.')
        # Determine whether we need HBounded storage.
        bpmx_on = (depth_bpmx is None) or (depth_bpmx > 0)
        pathmax_on = rule_pathmax is not None
        needs_storage = bpmx_on or pathmax_on
        chain = self._build_chain(h=h,
                                  bounds=bounds,
                                  auto_wrap=needs_storage)
        if needs_storage and self._find_hbounded(chain) is None:
            raise ValueError(
                'rule_pathmax / depth_bpmx require an HBounded '
                'in the heuristic chain as storage for lifted '
                'h values; pass `h` as a callable / None (will '
                'auto-wrap) or supply `bounds=...` (can be empty).')
        self._rule_pathmax: int | None = rule_pathmax
        self._depth_bpmx: int | None = depth_bpmx
        AStar.__init__(self,
                       problem=problem,
                       h=chain,
                       name=name,
                       is_recording=is_recording,
                       search_state=search_state)
        # 10-counter scaffold in 3 visual groups.
        self._counters = Counters(names=(
            ('cnt_pathmax_attempts',
             'cnt_pathmax_lifts'),
            ('cnt_bpmx_attempts',
             'cnt_bpmx_iterations',
             'cnt_bpmx_rule3_lifts',
             'cnt_bpmx_rule1_forwards',
             'cnt_bpmx_subtree_states'),
            ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ))

    # ──────────────────────────────────────────────────
    #  Heuristic Chain Builders
    # ──────────────────────────────────────────────────

    @staticmethod
    def _build_chain(h: HBase | Callable | None,
                     bounds: dict | None,
                     auto_wrap: bool) -> HBase:
        """
        ====================================================================
         Assemble the heuristic chain.

         Pre-built HBase: pass through. `bounds` cannot be supplied
         alongside (would double-wrap).

         Callable / None: wrap in HCallable (h=0 if None), then
         layer HBounded with the supplied bounds dict, or with
         an empty dict when `auto_wrap=True`.
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
    #  Counters (mirror frontier into the scaffold)
    # ──────────────────────────────────────────────────

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         Live snapshot of the 10-counter scaffold. Heap-op
         counts (cnt_push / cnt_pop / cnt_decrease) are the
         frontier's authoritative tally, mirrored in here on
         each access via `Counters.assign` (single source of
         truth: FrontierPriority).
        ====================================================================
        """
        fc = self._search.frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        self._counters.assign('cnt_decrease', fc['cnt_decrease'])
        return self._counters

    # ──────────────────────────────────────────────────
    #  Event Enrichment
    # ──────────────────────────────────────────────────

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         AStar handles push / pop / decrease_g (h, f).
         AStarBPMX adds int-casts for h_old / h_new on the
         pathmax / BPMX events.
        ====================================================================
        """
        AStar._enrich_event(self, event)
        t = event.get('type')
        if t in ('pathmax_apply', 'bpmx_lift', 'bpmx_forward'):
            for k in ('h_old', 'h_new'):
                if k in event:
                    event[k] = int(event[k])

    # ──────────────────────────────────────────────────
    #  Pre-Expand Hook
    # ──────────────────────────────────────────────────

    def _pre_expand(self, state: State) -> None:
        """
        ====================================================================
         Apply the isolated pathmax rule (if enabled) at depth 1
         around `state`, then run the BPMX(d) cascade (if
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

    def _apply_pathmax(self, state: State) -> None:
        """
        ====================================================================
         Apply `rule_pathmax` once at the immediate parent ->
         children neighborhood. No cascading.
        ====================================================================
        """
        rule = self._rule_pathmax
        self._counters.inc('cnt_pathmax_attempts')
        hb = self._find_hbounded(self._h)
        if hb is None:
            return   # defensive; __init__ should have caught
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
                       state: State,
                       children: list[State],
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 1 (Mero, 1984): parent -> child.
             h'(c) = max(h(c), h(p) - w(p, c)).
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
                       state: State,
                       children: list[State],
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 2 (Felner): children -> parent via min.
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
                       state: State,
                       children: list[State],
                       hb: HBounded) -> None:
        """
        ====================================================================
         Rule 3 (Felner): single child -> parent (reverse pathmax).
             h'(p) = max(h(p), max_c(h(c) - w(c, p))).
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

    def _apply_bpmx(self, state: State) -> None:
        """
        ====================================================================
         Felner Algorithm 2: BPMX(d) cascade.

         BFS-spans the d-level successor subtree from `state`,
         then iterates (Rule 3 bottom-up, Rule 1 top-down) until
         no pass tightens any node. `state` itself is the BFS
         root; cached descendants (perfect-h) are skipped from
         lift mutation.

         `depth = None` propagates through the full reachable
         subtree (visited-set bounded). Self-amortizes via the
         no-improvement short-circuit.
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        hb = self._find_hbounded(self._h)
        if hb is None:
            return   # defensive; __init__ should have caught
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
                       levels: list[list[State]],
                       edges: dict[State, list[State]],
                       hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 3 (single child -> parent) sweep, bottom-up over
         the BFS subtree. For each level k from d-1 down to 0,
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
                         levels: list[list[State]],
                         edges: dict[State, list[State]],
                         hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 1 (parent -> child) sweep, top-down over the BFS
         subtree. For each level k from 0 to d-1, each parent
         lifts every child at level k+1.

         Cached children skipped (h* cannot be tightened).
         Closed children NOT skipped: paper-aligned --
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
            root: State,
            depth: int | None,
            ) -> tuple[list[list[State]], dict[State, list[State]]]:
        """
        ====================================================================
         BFS spanning tree from `root` up to `depth` levels (or
         the full reachable subgraph when `depth is None`),
         visited-set bounded.

         Returns:
           levels: levels[k] = states at BFS depth k.
                   levels[0] = [root].
           edges:  state -> list of children in the spanning
                   tree (successors first-visited via that
                   state).

         The spanning tree loses graph edges where a descendant
         has multiple paths from the root. For admissibility this
         is fine -- any lift derived from the spanning tree is
         a valid lower bound. A DAG-aware variant (multi-parent
         edges) is a future optimisation.
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
