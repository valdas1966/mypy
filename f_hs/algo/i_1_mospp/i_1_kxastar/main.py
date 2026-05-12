from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_1_mospp._single_start_view import _SingleStartView
from f_hs.algo.i_1_mospp.i_0_base.main import (
    AlgoMOSPP, PHASE_SEARCH,
)
from f_hs.algo.i_1_mospp.mixins.extendable import ExtendableMOSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KxAStarMOSPP(Generic[State],
                   AlgoMOSPP[State],
                   ExtendableMOSPP[State]):
    """
    ============================================================================
     Repetitive k×A* (kxA*_min) for the Many-to-One Shortest
     Path Problem — the MOSPP **paper baseline**.

     Runs `k` INDEPENDENT A* sub-searches, one per start, with
     NO state sharing across sub-searches. Each sub-search
     begins at a different start, searches forward toward the
     **shared single goal**, builds its own `SearchStateSPP`
     from scratch, and is then discarded. The orchestrator
     aggregates per-start results into a `SolutionMOSPP`
     Mapping `{start: SolutionSPP}`.

     **Mirror of `KxAStarOMSPP`**. The structural shape is
     identical (k independent A*s with no state sharing). The
     axis is swapped:

       OMSPP: 1 start, k goals → iterate `problem.goals`,
              h varies per sub-search (closed over goal_i).
       MOSPP: k starts, 1 goal → iterate `problem.starts`,
              h is FIXED across sub-searches (closed once
              over the shared goal).

     The fixed-h property is the most notable structural
     consequence of the axis swap: kxA*-MOSPP precomputes the
     wrapped h callable once at __init__ and reuses it across
     every sub-search.

     Used as the **comparison baseline** for state-sharing
     MOSPP algorithms (future): k×A* expands each start's
     search tree independently, so cumulative `cnt_expanded`
     / `cnt_generated` is the upper bound that state-sharing
     algos aim to beat.

     **Assumptions / requirements:**

       - **Admissible heuristic** (consistency not required —
         no fast-path relies on it).
       - Edge costs non-negative (inherited from `ProblemSPP`
         / A* correctness).

     **Composes the `ExtendableMOSPP` capability mixin** with
     the same value boundary as `KxAStarOMSPP` composes
     `ExtendableOMSPP`:

       Useful here:
         - `extend(new_starts)` — append starts; run A* only
           on genuinely-new starts (the
           `already_reached` fast-path skips A* on duplicates).
         - `run_nested(problems, h, ...)` — classmethod
           convenience for prefix-extending problem sequences.
         - Cumulative counters / elapsed / recorder.

       Structurally inert here:
         - Lazy re-push of trailing reached start — no shared
           frontier; `_repush_last_reached_start` is a no-op.
         - Already-closed fast-path — no shared CLOSED set;
           the branch never fires.
         - PHASE_UPDATE / refresh_priorities — no shared
           frontier to refresh.

     Recording schema (subset of canonical MOSPP 5-event set;
     mirrors `KxAStarOMSPP`'s subset with `on_start` in
     place of `on_goal`):

       - `push`, `pop`, `decrease_g` — emitted by each inner
         AStar via the shared recorder.
       - `on_start` — per start at sub-search end. Payload:
         `state=start, g=cost, reason ∈ {expanded,
         already_reached, unreachable}, start_index`. The
         `already_closed` reason is never emitted (no shared
         CLOSED set).
       - `update_frontier` — NOT emitted (no
         between-sub-search transition).
    ============================================================================
    """

    # Counter scaffold mirrors KxAStarOMSPP — drops
    # `cnt_h_update` (no PHASE_UPDATE moment in kxA*).
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search',),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('cnt_expanded', 'cnt_generated'),
        ('mem_open', 'mem_closed'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'KxAStarMOSPP',
                 is_recording: bool = False,
                 is_timing: bool = True,
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `h` is a bi-arg callable `h(state, goal) -> int`. The
         goal is FIXED (MOSPP has a single goal), so the
         counter-wrapped h is built ONCE in __init__ — closed
         over `self._goal = self.problem.goals[0]` — and
         reused across every sub-search.

         No `cnt_h_update` counter (no PHASE_UPDATE).
         `elapsed_update` stays at 0.0 by design.
        ====================================================================
        """
        if len(problem.goals) != 1:
            raise ValueError(
                f'KxAStarMOSPP requires exactly 1 goal '
                f'(got {len(problem.goals)})')
        AlgoMOSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        # The fixed goal — captured once for the closure.
        self._goal: State = problem.goals[0]
        # Counter-wrapped h, built once and reused. Closure
        # captures `self._counters` and `self._goal`; every
        # call increments `cnt_h_search` and returns
        # `h(state, goal)`.
        self._h_wrapped: Callable[[State], int] = (
            self._make_h_wrapped())
        # ExtendableMOSPP bookkeeping — full start sequence
        # seen so far (across run + every extend), and the
        # trailing completed start. _last_algo is tracked for
        # contract symmetry but never consulted by
        # _repush_last_reached_start (no shared state to
        # push into).
        self._all_starts: list[State] = []
        self._last_reached_start: State | None = None
        self._last_algo: AStar[State] | None = None
        # Peak memory across sub-searches.
        self._mem_open_peak: int = 0
        self._mem_closed_peak: int = 0

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionMOSPP:
        """
        ====================================================================
         Run k independent A* sub-searches sequentially, one
         per start. Delegates the per-start loop body to
         `_handle_start`, shared with `ExtendableMOSPP.extend()`.
        ====================================================================
        """
        self._all_starts = list(self.problem.starts)
        self._last_reached_start = None
        self._last_algo = None
        self._mem_open_peak = 0
        self._mem_closed_peak = 0
        for i, start in enumerate(self._all_starts):
            self._handle_start(start, idx=i)
        return SolutionMOSPP(self._solutions)

    def _handle_start(self, start: State, idx: int) -> None:
        """
        ====================================================================
         Per-start sub-search body. Shared by `_run()` and
         `ExtendableMOSPP.extend()`.

         Skips A* on the `already_reached` fast-path when a
         prior sub-search (in this run, or any prior
         `extend()`) already finalized this start's cost.
        ====================================================================
        """
        # Fast-path: already solved by a prior sub-search. The
        # `already_closed` branch is omitted — kxA* has no
        # shared CLOSED set.
        if start in self._solutions:
            sol = self._solutions[start]
            self._emit_on_start(start, cost=sol.cost,
                                reason='already_reached',
                                start_index=idx)
            return

        # Build sub-problem (single-start view) and a FRESH
        # AStar instance. No `search_state=...` — each
        # sub-search owns its own bundle.
        sub_problem = _SingleStartView[State](
            base=self.problem, start=start)
        algo = AStar[State](
            problem=sub_problem,
            h=self._h_wrapped,
            name=f'{self.name}[{idx}]',
            is_recording=False,
        )
        # Share the recorder so push/pop/decrease_g events
        # from each sub-search land in the orchestrator's
        # event stream.
        algo._recorder = self._recorder
        # Phase stays SEARCH throughout (no UPDATE flips in
        # kxA*).
        self.phase = PHASE_SEARCH
        sol = algo.run()

        # Accumulate per-sub-search counters. Each sub-search
        # has its OWN frontier — there is no end-of-run sync
        # from a shared frontier, so we aggregate inline.
        ic = algo.counters
        self._counters.inc('cnt_expanded',
                           n=ic['cnt_expanded'])
        self._counters.inc('cnt_generated',
                           n=ic['cnt_generated'])
        self._counters.inc('cnt_push', n=ic['cnt_push'])
        self._counters.inc('cnt_pop', n=ic['cnt_pop'])
        self._counters.inc('cnt_decrease',
                           n=ic['cnt_decrease'])

        # Track peak memory.
        open_mem, closed_mem = self._mem_of(algo)
        if open_mem > self._mem_open_peak:
            self._mem_open_peak = open_mem
        if closed_mem > self._mem_closed_peak:
            self._mem_closed_peak = closed_mem

        # Emit on_start.
        reason = ('expanded' if sol.cost != float('inf')
                  else 'unreachable')
        self._emit_on_start(start, cost=sol.cost,
                            reason=reason, start_index=idx)
        self._solutions[start] = sol

        # ExtendableMOSPP bookkeeping.
        if reason == 'expanded':
            self._last_reached_start = start
            self._last_algo = algo
        else:
            self._last_reached_start = None
            self._last_algo = None

    def _repush_last_reached_start(self) -> None:
        """
        ====================================================================
         No-op for kxA*-MOSPP. There is no shared frontier to
         re-push into. Clearing the bookkeeping for hygiene.
        ====================================================================
        """
        self._last_reached_start = None
        self._last_algo = None

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         No-op. kxA* has no shared frontier; heap-op counters
         are accumulated inline in `_handle_start` per
         sub-search.
        ====================================================================
        """
        pass

    def _sync_memory_snapshot(self) -> None:
        """
        ====================================================================
         Write tracked peak memory across sub-searches into
         `self._counters`. Overrides the base auto-probe.
        ====================================================================
        """
        self._counters.assign('mem_open', self._mem_open_peak)
        self._counters.assign(
            'mem_closed', self._mem_closed_peak)

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, start: State) -> list[State]:
        """
        ====================================================================
         kxA* discards each sub-search's parent pointers after
         the sub-search completes (no persistent state). Path
         reconstruction is not supported — returns `[]`.
        ====================================================================
        """
        return []

    # ──────────────────────────────────────────────────
    #  Internal
    # ──────────────────────────────────────────────────

    def _make_h_wrapped(self) -> Callable[[State], int]:
        """
        ====================================================================
         Build the counter-wrapped unary h-function. Closes
         over `self._goal` (the fixed MOSPP goal) and
         `self._counters` once — the same callable is reused
         across every sub-search.
        ====================================================================
        """
        h_outer = self._h
        goal = self._goal
        counters = self._counters

        def h_wrapped(s: State) -> int:
            v = h_outer(s, goal)
            counters.inc('cnt_h_search')
            return v

        return h_wrapped

    def _emit_on_start(self,
                       start: State,
                       cost: float,
                       reason: str,
                       start_index: int,
                       ) -> None:
        """
        ====================================================================
         Emit an `on_start` event. Carries the start index so
         duplicate starts in `problem.starts` remain
         distinguishable. Mirror of OMSPP's `_emit_on_goal`.
        ====================================================================
        """
        if not self._recorder.is_active:
            return
        self._recorder.record(dict(
            type='on_start',
            state=start,
            g=(int(cost) if cost != float('inf') else cost),
            reason=reason,
            start_index=start_index,
        ))

    def _mem_of(self,
                algo: 'AStar[State]'
                ) -> tuple[int, int]:
        """
        ====================================================================
         Compute (open, closed) memory footprint for a
         completed sub-search's `SearchStateSPP`. Mirrors the
         per-entry split logic in
         `AlgoMOSPP._sync_memory_snapshot` so the cross-algo
         memory metric is comparable.
        ====================================================================
        """
        import sys
        ss = algo.search_state
        if ss is None or not hasattr(ss, 'frontier'):
            return (0, 0)
        frontier = ss.frontier
        closed = ss.closed
        g, parent = ss.g, ss.parent
        queue = getattr(frontier, '_queue', None)
        if queue is not None and hasattr(queue, '_heap'):
            frontier_struct = (sys.getsizeof(queue._heap)
                               + sys.getsizeof(queue._index)
                               + sum(sys.getsizeof(t)
                                     for t in queue._heap))
        else:
            frontier_struct = sys.getsizeof(
                queue if queue is not None else frontier)
        n_g = len(g)
        n_open = len(frontier)
        if n_g > 0:
            g_parent_total = (sys.getsizeof(g)
                              + sum(sys.getsizeof(v)
                                    for v in g.values())
                              + sys.getsizeof(parent))
            per_entry = g_parent_total / n_g
            g_parent_open = round(per_entry * n_open)
            g_parent_closed = round(per_entry * (n_g - n_open))
        else:
            g_parent_open = 0
            g_parent_closed = 0
        return (
            frontier_struct + g_parent_open,
            sys.getsizeof(closed) + g_parent_closed,
        )
