from time import perf_counter

from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_mospp._flipped_view import _FlippedView
from f_hs.algo.i_1_mospp._recorder_shim import _OnGoalToOnStartShim
from f_hs.algo.i_1_mospp.i_0_base.main import AlgoMOSPP, PHASE_SEARCH
from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
from f_hs.algo.u_mem import finalize_mem_total
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class KAStarIncMOSPP(Generic[State], AlgoMOSPP[State]):
    """
    ============================================================================
     Incremental kA* for the Many-to-One Shortest Path Problem
     via the axis-swap (flip-to-OMSPP) delegation.

     Solves the MOSPP (k starts -> 1 goal) by recognising that
     on an UNDIRECTED graph it is exactly the flip of an OMSPP
     (1 start -> k goals): build a `_FlippedView` (the MOSPP
     goal becomes the OMSPP shared start; the MOSPP starts
     become the OMSPP goals), delegate to the incremental
     OMSPP solver `KAStarInc`, then re-key the per-goal OMSPP
     solution as a per-start MOSPP solution. Because
     `dist(goal, start_i) == dist(start_i, goal)` on an
     undirected graph the per-start costs are exact; a path is
     recovered by reversing the OMSPP path.

     Sibling of `KBFSMOSPP` / `KDijkstraMOSPP` (same
     flip-delegation pattern) — but the inner solver is the
     INCREMENTAL kA*, which carries ONE shared `SearchStateSPP`
     across the k goals (a single growing search tree) rather
     than k independent passes. This is the OMSPP-side mirror
     of `AStarIncMOSPP`'s forward goal-anchored reuse: the
     same MOSPP instance solved by growing a search OUTWARD
     from the shared goal instead of running k forward
     searches into it.

     **Extendable (batch).** Unlike the per-start `extend()` of
     `AStarRepMOSPP` / `AStarIncMOSPP` (which compose
     `ExtendableMOSPP`), this wrapper does NOT iterate starts:
     it delegates a whole batch of new starts to the inner
     `KAStarInc.extend()` (which appends them as new OMSPP
     goals and grows the one shared search). So `extend()` is
     implemented directly here, batch-style, rather than via
     the per-start mixin — the mixin's `_handle_start` loop is
     the wrong granularity for a single-inner-search delegate.
     `run()` + `extend()` make a nested MOSPP chain solvable in
     one pass, exactly as the s_3 experiment drives the other
     incremental algos.

     **Correctness preconditions** (shared with KBFS/KDijkstra
     MOSPP):

       1. **Undirected graph** (or symmetric `successors` / `w`).
          The flipped view relabels which list is "starts" vs
          "goals"; it does NOT reverse adjacency. On a directed
          graph it silently computes the wrong quantity. No
          runtime check.
       2. **Consistent heuristic** — required by the inner
          `KAStarInc` (its same-nodes guarantee + the
          already-closed fast-path). Manhattan on grids is
          consistent. (Contrast `AStarIncMOSPP`, which works
          on directed graphs and tolerates inconsistent h.)
       3. **Exactly one goal** — `ValueError` at construction
          if `len(problem.goals) != 1`.

     **Counters** mirror the inner `KAStarInc` (search +
     heuristic + frontier + memory); `cnt_h_update` is exposed
     (the inter-sub-search refresh cost) alongside
     `cnt_h_search`. No BPMX / propagation / adaptive / cache-
     hit counters — this solver has none.
    ============================================================================
    """

    # Factory
    Factory: type = None

    # Mirror the inner KAStarInc scaffold (heuristic + search +
    # frontier) plus the MOSPP-base memory group.
    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search', 'cnt_h_update'),
        ('cnt_expanded', 'cnt_generated'),
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        ('mem_open', 'mem_closed', 'mem_total'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'KAStarIncMOSPP',
                 is_recording: bool = False,
                 is_timing: bool = True) -> None:
        """
        ====================================================================
         Validate exactly one goal, then delegate to
         `AlgoMOSPP.__init__`. `h` is the bi-arg MOSPP
         heuristic `h(state, goal)`; it is handed UNCHANGED to
         the inner `KAStarInc`, which calls it as
         `h(state, omspp_goal)` = `h(state, mospp_start_j)` —
         the correct OMSPP heuristic for the flipped search.
        ====================================================================
        """
        if len(problem.goals) != 1:
            raise ValueError(
                f'KAStarIncMOSPP requires exactly 1 goal '
                f'(got {len(problem.goals)})')
        AlgoMOSPP.__init__(self, problem=problem, h=h, name=name,
                           is_recording=is_recording,
                           is_timing=is_timing)
        self._inner: KAStarInc[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State] | None:
        """
        ====================================================================
         The inner `KAStarInc`'s shared `SearchStateSPP` bundle
         after `run()` (and any `extend()`). Drives the base
         `_sync_memory_snapshot` auto-probe.
        ====================================================================
        """
        return self._inner.search_state if self._inner else None

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionMOSPP:
        """
        ====================================================================
         Build the flipped (OMSPP) view, delegate to
         `KAStarInc`, re-key the per-goal solution as a
         per-start solution. The inner already keys by State
         (= MOSPP starts after the flip), so it is a direct
         copy (mirror of `KBFSMOSPP._run`).
        ====================================================================
        """
        flipped = _FlippedView[State](base=self.problem)
        self._inner = KAStarInc[State](
            problem=flipped,
            h=self._h,
            name=f'{self.name}[inner]',
            is_recording=False,
            is_timing=False,
        )
        # Route inner events through the shim: on_goal -> on_start.
        self._inner._recorder = _OnGoalToOnStartShim(self._recorder)
        self._inner.run()
        self._solutions = dict(self._inner.solutions)
        return SolutionMOSPP(self._solutions)

    def extend(self, new_starts: list[State]) -> SolutionMOSPP:
        """
        ====================================================================
         Resume with additional MOSPP starts (BATCH). The new
         starts ARE the new OMSPP goals after the flip, so a
         single `inner.extend(new_starts)` grows the one shared
         search to reach them — no per-start loop. Mirrors the
         `ExtendableMOSPP.extend()` timing / counter-sync
         epilogue so `extend()` leaves the orchestrator in the
         same consistent state as `run()`.

         Returns a `SolutionMOSPP` over the FULL set of starts
         seen so far (run + every extend). Counters / elapsed
         are cumulative (the inner accumulates).
        ====================================================================
        """
        if self._inner is None or self._elapsed is None:
            raise RuntimeError(
                'extend() requires a completed run() first')
        if not new_starts:
            raise ValueError('new_starts must be non-empty')

        t0 = perf_counter()
        if self._is_timing:
            self._t_phase_start = t0
        self._phase = PHASE_SEARCH

        # Batch-delegate: the new MOSPP starts are the new OMSPP
        # goals. The inner appends them and grows the shared search.
        self._inner.extend(new_starts)
        self._solutions = dict(self._inner.solutions)

        # Epilogue (mirror of AlgoMOSPP._run_post / the mixin's
        # extend tail): flush phase bucket, accumulate elapsed,
        # re-sync counters + memory, finalize mem_total LAST.
        self._flush_phase_timer()
        self._elapsed = (self._elapsed or 0.0) + (perf_counter() - t0)
        self._sync_frontier_counters()
        self._sync_memory_snapshot()
        finalize_mem_total(self._counters)
        return SolutionMOSPP(self._solutions)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the inner `KAStarInc`'s counters into this
         scaffold. The inner accumulates across run + extend,
         so `assign` (overwrite with the inner's current value)
         yields the cumulative total. Called by
         `AlgoMOSPP._run_post` and by `extend()`.
        ====================================================================
        """
        if self._inner is None:
            return
        ic = self._inner.counters
        for name in ('cnt_h_search', 'cnt_h_update',
                     'cnt_push', 'cnt_pop', 'cnt_decrease',
                     'cnt_expanded', 'cnt_generated'):
            self._counters.assign(name, ic[name])

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, start: State) -> list[State]:
        """
        ====================================================================
         Walk the inner OMSPP path (MOSPP goal -> ... -> start)
         and reverse it so the caller sees `[start, ..., goal]`
         in MOSPP direction. `[]` if `start` is unreachable.
        ====================================================================
        """
        if self._inner is None:
            return []
        return list(reversed(self._inner.reconstruct_path(start)))
