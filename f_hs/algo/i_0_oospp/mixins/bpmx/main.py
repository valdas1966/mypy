from typing import TYPE_CHECKING

from f_core.counters.main import Counters
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded

if TYPE_CHECKING:
    pass


class BPMXMixin:
    """
    ============================================================================
     Mixin: Felner pathmax / BPMX cascade as a reusable
     in-search mechanism.

     Hosts the search-time pathmax mechanics so its host
     class can compose them without duplicating code:
       - AStarLookup (AStarLookup + BPMXMixin) — cache /
         bounds / propagate_pathmax + (optional) BPMX in one
         pass; the canonical advanced-A* class (used by
         k×A*-CB). The mixin's sole consumer.

     Faithful to Felner et al., "Inconsistent Heuristics in
     Theory and Practice", AIJ 2011 (rules §5.1–5.3,
     cascade Algorithm 2).

     Single-axis API: `rule_bpmx ∈ {None, '1', '2', '3',
     'CASCADE'}` selects what runs; `depth_bpmx ∈ {None,
     int >= 1}` controls how far it walks.

       - `'1'`  Rule 1 (Mero, 1984) — parent → child:
                  h'(c) = max(h(c), h(p) − w(p, c)).
                  Top-down sweep over BFS subtree to
                  `depth_bpmx` levels (default 1 = isolated).

       - `'2'`  Rule 2 (Felner) — children → parent via min:
                  h'(p) = max(h(p),
                              min_i(h(c_i) + w(p, c_i))).
                  Structurally depth-1 only — Rule 2's operator
                  consumes "a parent + its full children set",
                  which has no chained-grandparent analogue.
                  Constructor enforces `depth_bpmx == 1`.

       - `'3'`  Rule 3 (Felner) — strongest child → parent:
                  h'(p) = max(h(p),
                              max_c(h(c) − w(c, p))).
                  Bottom-up sweep over BFS subtree to
                  `depth_bpmx` levels (default 1 = isolated).

       - `'CASCADE'`  Felner Algorithm 2 — Rules 1 + 3
                  alternating, iterated to fixed point over the
                  d-level BFS subtree. The bidirectional pathmax
                  propagation that gives BPMX its name.

     Why deep Rule 1 / Rule 3 alone? Cascade is strictly ≥
     either single-direction sweep but does roughly 2× the
     work and iterates. Single-direction sweeps trade some
     lift coverage for cheaper per-expansion overhead — useful
     for ablation studies.

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
       - `_pre_expand(state)` override (orchestrates the
         selected rule).
       - `counters` property (mechanism counters + frontier /
         memory mirror).
       - `_enrich_event(event)` (int-casts BPMX h_old / h_new;
         chains to next class in MRO via super()).
       - `_init_bpmx_mechanism(rule_bpmx, depth_bpmx)`
         — call from host's __init__ after AStar.__init__.

     MRO contract: place BPMXMixin BEFORE AStar / AlgoSPP in
     the host class's bases so `_pre_expand`, `counters`, and
     `_enrich_event` resolve here first. Example:

         class AStarLookup(BPMXMixin, AStar[State],
                           Generic[State]):
             ...
    ============================================================================
    """

    _VALID_RULE_BPMX: frozenset[str | None] = frozenset(
        {None, '1', '2', '3', 'CASCADE'})

    # 3-counter mechanism scaffold. `cnt_bpmx_depth` is a max
    # tracker (deepest BFS-level at which a lift fired across
    # the run), updated via assign; the others are cumulative
    # via inc. Frontier (3) and memory (4) groups round out the
    # default scaffold; AStarLookup overrides via
    # `_COUNTER_NAMES` to prepend the propagate group.
    _BPMX_COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_bpmx_attempts',
         'cnt_bpmx_successes',
         'cnt_bpmx_depth'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed',
         'mem_cache', 'mem_bounds'),
    )

    # ──────────────────────────────────────────────────
    #  Validators (static; for use in host __init__)
    # ──────────────────────────────────────────────────

    @classmethod
    def _validate_rule_bpmx(cls, rule_bpmx: str | None) -> None:
        """
        ====================================================================
         Validate `rule_bpmx` ∈ {None, '1', '2', '3', 'CASCADE'}.
         Raises ValueError otherwise.
        ====================================================================
        """
        if rule_bpmx not in cls._VALID_RULE_BPMX:
            valid = sorted(v for v in cls._VALID_RULE_BPMX
                           if v is not None)
            raise ValueError(
                f"rule_bpmx must be one of {valid} or None; "
                f"got {rule_bpmx!r}")

    @staticmethod
    def _validate_depth_bpmx(depth_bpmx: int | None) -> None:
        """
        ====================================================================
         Validate `depth_bpmx` ∈ {None} ∪ {int >= 1}. Rejects
         bool (guards `True` / `False` typos), 0, and negatives.
        ====================================================================
        """
        if depth_bpmx is None:
            return
        if (not isinstance(depth_bpmx, int)
                or isinstance(depth_bpmx, bool)
                or depth_bpmx < 1):
            raise ValueError(
                f"depth_bpmx must be int >= 1 or None; got "
                f"{depth_bpmx!r}")

    @classmethod
    def _validate_combination(cls,
                              rule_bpmx: str | None,
                              depth_bpmx: int | None) -> None:
        """
        ====================================================================
         Cross-axis validation. Rule 2 cannot propagate beyond
         depth 1 — its operator consumes a parent + its full
         children set, which has no chained-grandparent
         analogue. `depth_bpmx is None` (full reach) and
         `depth_bpmx > 1` are both rejected for Rule 2.
        ====================================================================
        """
        if rule_bpmx == '2' and depth_bpmx != 1:
            raise ValueError(
                "rule_bpmx='2' requires depth_bpmx=1; Rule 2's "
                "operator consumes a parent + its full children "
                "set and has no chained-grandparent analogue. "
                "For deep propagation use 'CASCADE' or '1' / '3' "
                f"with depth_bpmx > 1; got depth_bpmx={depth_bpmx!r}")

    # ──────────────────────────────────────────────────
    #  Chain Inspector (static; HBounded lookup)
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

    # ──────────────────────────────────────────────────
    #  Initialization (called from host __init__)
    # ──────────────────────────────────────────────────

    def _init_bpmx_mechanism(self,
                             rule_bpmx: str | None,
                             depth_bpmx: int | None) -> None:
        """
        ====================================================================
         Initialize the mechanism state and the counter
         scaffold. Call from the host class's __init__ AFTER
         the AStar.__init__ chain has set `self._h`,
         `self._search`, etc.

         Scaffold resolution: if the host class declares its
         own `_COUNTER_NAMES` class attribute, that wins
         (per-class override pattern). Otherwise the mixin's
         `_BPMX_COUNTER_NAMES` default is used. AStarLookup
         overrides to add the `cnt_prop_*` group from its
         pre-search `propagate_pathmax`.
        ====================================================================
        """
        self._rule_bpmx: str | None = rule_bpmx
        self._depth_bpmx: int | None = depth_bpmx
        names = getattr(type(self), '_COUNTER_NAMES',
                        self._BPMX_COUNTER_NAMES)
        self._counters: Counters = Counters(names=names)

    # ──────────────────────────────────────────────────
    #  Counters property (mechanism + frontier mirror)
    # ──────────────────────────────────────────────────

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         Live snapshot of the scaffold. Heap-op counts
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
    #  Event Enrichment (chains to next class in MRO)
    # ──────────────────────────────────────────────────

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Add int-cast for `h_old` / `h_new` on pathmax / BPMX
         events. Chains to next `_enrich_event` in MRO via
         super() — for AStarLookup that's AStar (h, f), and
         AStarLookup's own override layers is_cached /
         is_bounded / propagate casts on top (it calls super()
         first, so this mixin's int-casts run BEFORE
         AStarLookup's flags).
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
         Apply the configured BPMX rule on `state`. Delegates
         to `_apply_bpmx` which dispatches by `rule_bpmx`:
           - None       → no-op
           - '1' / '3'  → single-direction sweep over the
                           depth-d BFS subtree (no iteration)
           - '2'        → isolated min-children → parent (depth 1)
           - 'CASCADE'  → Felner Algorithm 2 (Rules 1 + 3,
                           alternating sweeps, iterated to
                           fixed point)
        ====================================================================
        """
        if self._rule_bpmx is None:
            return
        self._apply_bpmx(state=state)

    # ──────────────────────────────────────────────────
    #  Lift-depth tracker (max via assign)
    # ──────────────────────────────────────────────────

    def _record_lift_at_level(self, level: int) -> None:
        """
        ====================================================================
         Update `cnt_bpmx_depth` to max(current, level) via
         assign. Called on each successful lift, with `level`
         being the BFS-depth (0 = root) of the LIFTED node.
        ====================================================================
        """
        if level > self._counters['cnt_bpmx_depth']:
            self._counters.assign('cnt_bpmx_depth', level)

    # ──────────────────────────────────────────────────
    #  Mechanism dispatch
    # ──────────────────────────────────────────────────

    def _apply_bpmx(self, state) -> None:
        """
        ====================================================================
         Dispatch by `rule_bpmx`. Increments
         `cnt_bpmx_attempts` once per call (regardless of
         whether any lift fires).
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        hb = self._find_hbounded(self._h)
        if hb is None:
            return
        rule = self._rule_bpmx
        self._counters.inc('cnt_bpmx_attempts')

        if rule == '2':
            children = list(self.problem.successors(state))
            if not children:
                return
            self._apply_rule2(state=state, children=children, hb=hb)
            return

        # Rules '1', '3', 'CASCADE': BFS-span the subtree first.
        levels, edges = self._collect_bpmx_subtree(
            root=state, depth=self._depth_bpmx)
        if rule == '1':
            self._sweep_rule1_down(levels=levels, edges=edges, hb=hb)
        elif rule == '3':
            self._sweep_rule3_up(levels=levels, edges=edges, hb=hb)
        elif rule == 'CASCADE':
            self._cascade(state=state, levels=levels,
                          edges=edges, hb=hb)

    # ──────────────────────────────────────────────────
    #  Rule 2 — isolated, depth 1 only
    # ──────────────────────────────────────────────────

    def _apply_rule2(self,
                     state,
                     children: list,
                     hb: HBounded) -> None:
        """
        ====================================================================
         Rule 2 (Felner): children → parent via min.
             h'(p) = max(h(p), min_i(h(c_i) + w(p, c_i))).
         Depth-1 only by structural constraint (constructor
         enforces depth_bpmx == 1).
        ====================================================================
        """
        if self._h.is_perfect(state):
            return
        h_p_old = self._h(state)
        cand = min(self._h(c) + self.problem.w(parent=state, child=c)
                   for c in children)
        if cand > h_p_old:
            hb.add_bound(state=state, value=cand)
            self._counters.inc('cnt_bpmx_successes')
            self._record_lift_at_level(0)
            self._record_event(
                type='pathmax_apply',
                state=state,
                rule=2,
                h_old=h_p_old,
                h_new=cand,
                via_children=tuple(children),
            )

    # ──────────────────────────────────────────────────
    #  Rule 3 — bottom-up sweep (used alone or in cascade)
    # ──────────────────────────────────────────────────

    def _sweep_rule3_up(self,
                        levels: list[list],
                        edges: dict,
                        hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 3 (single child → parent) sweep, bottom-up over
         the BFS subtree. For each level k from len(levels)-2
         down to 0, each parent at level k lifts from its
         strongest child at level k+1.

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
                    self._counters.inc('cnt_bpmx_successes')
                    self._record_lift_at_level(k)
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
    #  Rule 1 — top-down sweep (used alone or in cascade)
    # ──────────────────────────────────────────────────

    def _sweep_rule1_down(self,
                          levels: list[list],
                          edges: dict,
                          hb: HBounded) -> bool:
        """
        ====================================================================
         Rule 1 (parent → child) sweep, top-down over the BFS
         subtree. For each level k from 0 to len(levels)-2,
         each parent lifts every child at level k+1.

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
                        self._counters.inc('cnt_bpmx_successes')
                        self._record_lift_at_level(k + 1)
                        self._record_event(
                            type='bpmx_forward',
                            state=c,
                            h_old=h_c_old,
                            h_new=cand,
                            via_parent=p,
                        )
                        changed = True
        return changed

    # ──────────────────────────────────────────────────
    #  CASCADE — Felner Algorithm 2 (Rules 1 + 3 iterated)
    # ──────────────────────────────────────────────────

    def _cascade(self,
                 state,
                 levels: list[list],
                 edges: dict,
                 hb: HBounded) -> None:
        """
        ====================================================================
         Felner Algorithm 2: alternate Rule 3 bottom-up and
         Rule 1 top-down sweeps until neither tightens any
         node. Self-amortizes via the no-improvement
         short-circuit.
        ====================================================================
        """
        n_states = sum(len(L) for L in levels)
        iteration = 0
        while True:
            iteration += 1
            self._record_event(
                type='bpmx_iteration',
                state=state,
                iteration=iteration,
                num_levels=len(levels),
                num_states=n_states,
            )
            up = self._sweep_rule3_up(levels=levels, edges=edges, hb=hb)
            down = self._sweep_rule1_down(levels=levels, edges=edges, hb=hb)
            if not (up or down):
                break

    # ──────────────────────────────────────────────────
    #  BFS subtree collection (shared)
    # ──────────────────────────────────────────────────

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
