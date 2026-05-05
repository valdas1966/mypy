import sys

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

     Provides a minimal counter scaffold (composed via
     `f_core.counters.Counters`) holding only what every OMSPP
     algorithm tracks unconditionally:
       - Heap-op counts (frontier-sourced): `cnt_push`,
         `cnt_pop`, `cnt_decrease`.
       - End-of-search memory snapshot: `mem_open`,
         `mem_closed`.

     Counters are reset in `_run_pre()` before every `run()`.

     **Subclasses override `_COUNTER_NAMES`** to declare their
     own scaffold — adding mechanism-specific counters (e.g.,
     `cnt_h_*`, `cnt_phi_*`, `cnt_pop_stale`) and dropping any
     that don't apply. Hierarchy via class inheritance: the
     attribute resolves to the most-derived class's
     declaration, so `__init__` reads the right shape. Each
     algorithm's scaffold reflects exactly what it tracks; no
     structural zeros for unsupported mechanisms. Cross-algo
     comparison tooling unions counter sets when needed
     (`pd.DataFrame(rows).fillna(0)`).
    ============================================================================
    """

    # Factory
    Factory: type = None

    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        # Search-semantic group — incremented by orchestrators
        # (KAStarAgg directly; KAStarInc / KBFS / KDijkstra by
        # accumulating inner sub-search totals).
        ('cnt_expanded', 'cnt_generated'),
        # Memory snapshots — populated by _run_post() AFTER
        # _elapsed is recorded (outside the runtime budget).
        # mem_open / mem_closed split g/parent slot cost by
        # current OPEN/CLOSED membership (states not in OPEN
        # are charged to mem_closed).
        ('mem_open', 'mem_closed'),
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
         AStar `run` / `resume` calls + lazy re-push of reached
         non-last goals; Agg: main best-first loop body
         INCLUDING any lazy stale-pop re-checks that happen
         during search). Reset to 0.0 in `_run_pre()`. Stays
         0.0 when `is_timing=False`.
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
         frontier-owned counters into the algo's scaffold and
         take the end-of-search memory snapshot. All happen
         AFTER the inherited `_run_post` records `_elapsed`.
         The memory snapshot is therefore structurally OUT of
         the runtime budget.
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
        super()._run_post()                  # records _elapsed
        self._sync_frontier_counters()
        self._sync_memory_snapshot()         # outside _elapsed

    def _sync_memory_snapshot(self) -> None:
        """
        ====================================================================
         Default implementation: locate the snapshot state via
         common attribute names and write `mem_open`,
         `mem_closed`, `mem_g_parent` into `self._counters`.

         Probes (in order):
           1. `self._shared_state` (KAStarInc — SearchStateSPP).
           2. `self._search` (legacy fallback).
           3. `self._inner.search_state` (KBFS, KDijkstra —
              composed inner sub-algo).
           4. Direct attrs `self._frontier / _closed / _g /
              _parent` (KAStarAgg).

         Subclasses with non-standard state shapes can override.
        ====================================================================
        """
        ss = (getattr(self, '_shared_state', None)
              or getattr(self, '_search', None))
        if ss is None:
            inner = getattr(self, '_inner', None)
            if inner is not None:
                ss = getattr(inner, 'search_state', None)
        if ss is not None and hasattr(ss, 'frontier'):
            frontier, closed = ss.frontier, ss.closed
            g, parent = ss.g, ss.parent
        elif hasattr(self, '_frontier'):
            frontier = self._frontier
            closed = getattr(self, '_closed', set())
            g = getattr(self, '_g', {})
            parent = getattr(self, '_parent', {})
        else:
            return
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
        self._counters.assign('mem_open',
                              frontier_struct + g_parent_open)
        self._counters.assign(
            'mem_closed',
            sys.getsizeof(closed) + g_parent_closed)

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
