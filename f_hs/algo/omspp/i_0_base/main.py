from f_core.counters.main import Counters
from f_cs.algo import Algo
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)

# Phase tags — used for both counter routing (subclass-specific)
# and structural time bucketing (`elapsed_search` / `elapsed_update`).
PHASE_SEARCH = 'search'
PHASE_UPDATE = 'update'


class AlgoOMSPP(Generic[State],
                Algo[ProblemSPP[State], SolutionOMSPP]):
    """
    ============================================================================
     Abstract base for One-to-Many Shortest Path Problem
     algorithms (KAStarInc, KAStarAgg, future KDijkstra).

     Inherits the standard f_cs Algo lifecycle:

         run()  →  _run_pre  →  _run  →  _run_post

     `elapsed` (wall-clock) and `recorder` are auto-managed by
     ProcessBase / Algo. Subclasses override `_run()` to execute
     the algorithm body and return a `SolutionOMSPP`.

     Provides a unified 8-counter scaffold (composed via
     `f_core.counters.Counters`) so cross-algorithm benchmarks
     (KAStarAgg vs KAStarInc) can produce a uniform metric
     table. Counters are reset in `_run_pre()` before every
     `run()`. Each subclass increments whichever subset it
     supports (others stay at 0; document with reason in the
     subclass CLAUDE.md).

     The 8 counters (declared as 3 visual groups for `repr`):
       cnt_h_search    — h(state, goal) calls in normal flow.
       cnt_h_update    — h(state, goal) calls in refresh flow
                         (post-goal F refresh / inter-sub-search
                         priority refresh).

       cnt_phi_search  — `_compute_F` calls in normal flow
                         (Φ-aggregation algorithms only).
       cnt_phi_update  — `_compute_F` calls in refresh flow
                         (Φ-aggregation algorithms only).

       cnt_push        — frontier.push calls.
       cnt_pop         — frontier.pop calls.
       cnt_pop_stale   — subset of cnt_pop: stale-F re-insertions
                         (lazy-mode algorithms only).
       cnt_decrease    — frontier.decrease calls.
    ============================================================================
    """

    # Factory
    Factory: type = None

    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_h_search', 'cnt_h_update'),
        ('cnt_phi_search', 'cnt_phi_update'),
        ('cnt_push', 'cnt_pop',
         'cnt_pop_stale', 'cnt_decrease'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'AlgoOMSPP',
                 is_recording: bool = False,
                 is_timing: bool = True) -> None:
        """
        ========================================================================
         Init private Attributes.

         `is_timing` — when True (default), the `phase` property
         setter accumulates wall-clock into `elapsed_search` /
         `elapsed_update` buckets via `perf_counter`. Set False
         to skip the perf_counter call on every flip — useful
         for distortion-free wall-clock measurements at large
         k. Both timing properties stay at 0.0 when off.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        self._h: Callable[[State, State], int] = h
        self._solutions: dict[State, SolutionSPP] = {}
        self._counters: Counters = Counters(
            names=self._COUNTER_NAMES)
        # Structural-phase time bucketing.
        self._is_timing: bool = is_timing
        self._phase: str = PHASE_SEARCH
        self._t_phase_start: float = 0.0
        self._t_search: float = 0.0
        self._t_update: float = 0.0

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def solutions(self) -> dict[State, SolutionSPP]:
        """
        ====================================================================
         Per-goal `{goal: SolutionSPP}` populated by `_run()`.
         Same dict that the returned `SolutionOMSPP` wraps.
        ====================================================================
        """
        return self._solutions

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         Per-run operation counters as a `Counters` instance
         (Mapping protocol — `c[name]`, `dict(c)`, `c.items()`,
         `c == {...}` all work). Reset to 0 in `_run_pre()`,
         so `algo.counters` after `run()` reflects the most
         recent run only.
        ====================================================================
        """
        return self._counters

    @property
    def elapsed_search(self) -> float:
        """
        ====================================================================
         Wall-clock seconds spent in the **search** structural
         phase — i.e., inside the actual sub-search loops (Inc:
         AStar `run` / `resume` calls + force-expand; Agg: main
         best-first loop body INCLUDING any lazy stale-pop
         re-checks that happen during search). Reset to 0.0 in
         `_run_pre()`. Stays 0.0 when `is_timing=False`.
        ====================================================================
        """
        return self._t_search

    @property
    def elapsed_update(self) -> float:
        """
        ====================================================================
         Wall-clock seconds spent in the **update** structural
         phase — i.e., explicit between-sub-search work (Inc:
         `_emit_frontier_transition` + `algo.refresh_priorities`;
         Agg-eager: `_refresh_all_F` calls). Agg-lazy reports
         0.0 here by construction (no between-phase moment;
         refresh work happens inline during search). Reset to
         0.0 in `_run_pre()`. Stays 0.0 when `is_timing=False`.
        ====================================================================
        """
        return self._t_update

    @property
    def phase(self) -> str:
        """
        ====================================================================
         Current structural phase (`'search'` or `'update'`).
         Read-side; mutate via the setter only.
        ====================================================================
        """
        return self._phase

    @phase.setter
    def phase(self, value: str) -> None:
        """
        ====================================================================
         Flip the structural phase tag and accumulate elapsed
         wall-clock into the previous bucket. Idempotent (no
         work when value matches current). When
         `is_timing=False`, becomes a plain field write.
        ====================================================================
        """
        if value not in (PHASE_SEARCH, PHASE_UPDATE):
            raise ValueError(
                f'unknown phase {value!r}; '
                f'expected one of {PHASE_SEARCH!r}, '
                f'{PHASE_UPDATE!r}')
        if not self._is_timing:
            self._phase = value
            return
        if value == self._phase:
            return
        now = perf_counter()
        delta = now - self._t_phase_start
        if self._phase == PHASE_SEARCH:
            self._t_search += delta
        else:
            self._t_update += delta
        self._phase = value
        self._t_phase_start = now

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run_pre(self) -> None:
        """
        ====================================================================
         Reset wall-clock + per-run mutable state (counters,
         solutions dict, phase + bucket timers). Called
         automatically by Algo.run() before _run().
        ====================================================================
        """
        super()._run_pre()
        self._counters.reset()
        self._solutions = {}
        # Phase-bucket timer reset. Direct field writes are safe
        # here — nothing accumulated yet, no flush needed.
        self._t_search = 0.0
        self._t_update = 0.0
        self._phase = PHASE_SEARCH
        self._t_phase_start = perf_counter()

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Subclass override point. Execute the algorithm and
         return a `SolutionOMSPP` wrapping `self._solutions`.
        ====================================================================
        """
        raise NotImplementedError

    def _run_post(self) -> None:
        """
        ====================================================================
         Final flush of the active phase bucket, then sync
         frontier-owned counters into the algo's 8-counter
         scaffold. Both happen AFTER the inherited `_run_post`
         records `_elapsed`. The frontier is the single source
         of truth for `cnt_push` / `cnt_pop` / `cnt_decrease`;
         this hook mirrors the final tally onto `self._counters`
         so callers see all 8 counters via `algo.counters`.
        ====================================================================
        """
        # Flush the trailing phase bucket BEFORE inherited post,
        # so timing buckets reflect the full _run() span.
        if self._is_timing:
            now = perf_counter()
            delta = now - self._t_phase_start
            if self._phase == PHASE_SEARCH:
                self._t_search += delta
            else:
                self._t_update += delta
            self._t_phase_start = now
        super()._run_post()
        self._sync_frontier_counters()

    # ──────────────────────────────────────────────────
    #  Subclass Hooks
    # ──────────────────────────────────────────────────

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Subclass hook: mirror the frontier's
         `cnt_push` / `cnt_pop` / `cnt_decrease` into
         `self._counters` via `Counters.assign`. Default is a
         no-op (subclasses without a frontier — or that don't
         want to expose its counts — leave this alone).

         KAStarAgg reads its own `self._frontier`. KAStarInc
         reads the shared frontier on
         `self._shared_state.frontier`.
        ====================================================================
        """
        pass
