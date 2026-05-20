import sys

from f_core.counters.main import Counters
from f_cs.algo import Algo
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)

# Phase tags — same constants as AlgoOMSPP. Used for both
# counter routing (subclass-specific) and structural time
# bucketing (`elapsed_search` / `elapsed_update`).
PHASE_SEARCH = 'search'
PHASE_UPDATE = 'update'


class AlgoMOSPP(Generic[State],
                Algo[ProblemSPP[State], SolutionMOSPP]):
    """
    ============================================================================
     Abstract base for Many-to-One Shortest Path Problem
     algorithms.

     **Sibling of `AlgoOMSPP`** — both inherit the standard
     `f_cs.algo.Algo` lifecycle:

         run()  →  _run_pre  →  _run  →  _run_post

     `elapsed` (wall-clock) and `recorder` are auto-managed by
     `ProcessBase` / `Algo`. Subclasses override `_run()` to
     execute the algorithm body and return a `SolutionMOSPP`
     (Mapping over `{start: SolutionSPP}`).

     The MOSPP problem shape is `ProblemSPP` with
     `len(starts)=k, len(goals)=1` — k starts, one shared
     goal. The orchestrator iterates `self.problem.starts`
     and runs k sub-searches, one per start.

     Counter scaffold identical to `AlgoOMSPP`'s minimal set
     — subclasses override `_COUNTER_NAMES` to declare their
     own schema (heap-op + search-semantic + memory, with
     mechanism-specific extensions like `cnt_h_search`).
    ============================================================================
    """

    # Factory
    Factory: type = None

    _COUNTER_NAMES: tuple[tuple[str, ...], ...] = (
        ('cnt_push', 'cnt_pop', 'cnt_decrease'),
        # Search-semantic group — incremented by orchestrators
        # (e.g., AStarRepMOSPP accumulates inner sub-search
        # totals per iteration).
        ('cnt_expanded', 'cnt_generated'),
        # Memory snapshots — populated by _run_post() AFTER
        # _elapsed is recorded (outside the runtime budget).
        # `mem_open` uses `frontier.max_size` (rule-2; lifetime
        # peak |OPEN|); `mem_total = Σ mem_*` is the
        # conservative upper-bound coincident peak (component
        # peaks need not be simultaneous).
        ('mem_open', 'mem_closed', 'mem_total'),
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'AlgoMOSPP',
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
         Per-start `{start: SolutionSPP}` populated by `_run()`.
         Same dict that the returned `SolutionMOSPP` wraps.
        ====================================================================
        """
        return self._solutions

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         Per-run operation counters as a `Counters` instance
         (Mapping protocol). Reset to 0 in `_run_pre()`.
        ====================================================================
        """
        return self._counters

    @property
    def elapsed_search(self) -> float:
        """
        ====================================================================
         Wall-clock seconds spent in PHASE_SEARCH. Reset in
         `_run_pre()`. 0.0 when `is_timing=False`.
        ====================================================================
        """
        return self._t_search

    @property
    def elapsed_update(self) -> float:
        """
        ====================================================================
         Wall-clock seconds spent in PHASE_UPDATE. Reset in
         `_run_pre()`. 0.0 when `is_timing=False`.
        ====================================================================
        """
        return self._t_update

    @property
    def phase(self) -> str:
        """
        ====================================================================
         Current structural phase (`'search'` / `'update'`).
         Mutate via the setter only.
        ====================================================================
        """
        return self._phase

    @phase.setter
    def phase(self, value: str) -> None:
        """
        ====================================================================
         Flip the structural phase tag and accumulate elapsed
         wall-clock into the previous bucket. Idempotent.
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
         Reset wall-clock + per-run mutable state.
        ====================================================================
        """
        super()._run_pre()
        self._counters.reset()
        self._solutions = {}
        self._t_search = 0.0
        self._t_update = 0.0
        self._phase = PHASE_SEARCH
        self._t_phase_start = perf_counter()

    def _run(self) -> SolutionMOSPP:
        """
        ====================================================================
         Subclass override point. Execute the algorithm and
         return a `SolutionMOSPP` wrapping `self._solutions`.
        ====================================================================
        """
        raise NotImplementedError

    def _run_post(self) -> None:
        """
        ====================================================================
         Flush phase timer, then super (records `_elapsed`),
         then sync frontier counters + memory snapshot, then
         finalize `mem_total = Σ mem_*` last. `finalize_mem_total`
         after `_sync_memory_snapshot` so subclass overrides
         (e.g., `AStarIncMOSPP` adding `mem_cache` / `mem_bounds`)
         are auto-absorbed.
        ====================================================================
        """
        from f_hs.algo.u_mem import finalize_mem_total
        self._flush_phase_timer()
        super()._run_post()
        self._sync_frontier_counters()
        self._sync_memory_snapshot()
        finalize_mem_total(self._counters)

    def _flush_phase_timer(self) -> None:
        """
        ====================================================================
         Accumulate wall-clock since `_t_phase_start` into the
         current phase bucket and re-anchor. No-op when
         `is_timing=False`. Shared by `_run_post` and the
         `ExtendableMOSPP` mixin's `extend()`.
        ====================================================================
        """
        if not self._is_timing:
            return
        now = perf_counter()
        delta = now - self._t_phase_start
        if self._phase == PHASE_SEARCH:
            self._t_search += delta
        else:
            self._t_update += delta
        self._t_phase_start = now

    def _sync_memory_snapshot(self) -> None:
        """
        ====================================================================
         Default implementation: locate the snapshot state via
         common attribute names and write `mem_open`,
         `mem_closed` into `self._counters`. Same probe order
         as `AlgoOMSPP._sync_memory_snapshot`.
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
        # Rule-2 fix: peak |OPEN| over the whole run, not the
        # post-loop snapshot. Mirrors `AlgoSPP._memory_snapshot`
        # and `AlgoOMSPP._sync_memory_snapshot`.
        n_open_peak = min(
            getattr(frontier, 'max_size', len(frontier)), n_g)
        if n_g > 0:
            g_parent_total = (sys.getsizeof(g)
                              + sum(sys.getsizeof(v)
                                    for v in g.values())
                              + sys.getsizeof(parent))
            per_entry = g_parent_total / n_g
            g_parent_open = round(per_entry * n_open_peak)
            g_parent_closed = round(per_entry * (n_g - n_open_peak))
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
         Subclass hook: mirror frontier counters into
         `self._counters` via `Counters.assign`. Default
         no-op.
        ====================================================================
        """
        pass
