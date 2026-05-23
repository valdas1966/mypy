from f_hs.algo.i_1_mospp.i_0_base.main import PHASE_SEARCH
from f_hs.solution.main import SolutionMOSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class ExtendableMOSPP(Generic[State]):
    """
    ============================================================================
     Capability mixin: MOSPP orchestrator supports
     **prefix-extending** the START sequence after `run()`
     completes.

     Sibling of `ExtendableOMSPP` (OMSPP scope). Same shape,
     different axis:

       OMSPP: `extend(new_goals)` adds goals; hook
              `_handle_goal(goal, idx)`.
       MOSPP: `extend(new_starts)` adds starts; hook
              `_handle_start(start, idx)`.

     Composed by orchestrators whose `_run()` body is a
     per-start sub-search loop (today: `AStarRepMOSPP`).
     Provides the shared `extend(new_starts)` body and the
     `run_nested(problems, h)` classmethod convenience.
     Subclasses provide two hooks:

       - `_handle_start(start, idx)` — per-start sub-search
         body, shared between `_run()` and `extend()`.
       - `_repush_last_reached_start()` — re-push the
         previous run's last completed start onto OPEN (mirror
         of the OMSPP `_repush_last_reached_goal` contract;
         structurally inert for kxA*-flavored MOSPP since no
         shared frontier exists).

     The mixin assumes composition with `AlgoMOSPP` and reads
     `self._all_starts`, `self._solutions`, `self._counters`,
     `self._recorder`, `self._elapsed`, `self._is_timing`,
     `self._phase`, `self._t_phase_start`. It calls
     `self._flush_phase_timer()`,
     `self._sync_frontier_counters()`, and
     `self._sync_memory_snapshot()` on `AlgoMOSPP`.

     Why a parallel mixin (not generalized): the OMSPP and
     MOSPP mixin bodies are short orchestration shells with
     axis-specific naming (`new_goals` vs `new_starts`,
     `_handle_goal` vs `_handle_start`). Generalizing would
     force OMSPP code rename for zero behavioral benefit.
     The duplication is ~30 LOC and the naming clarity is
     worth it.
    ============================================================================
    """

    # Type-hint declarations — concrete values set by the
    # subclass __init__ / _run.
    _all_starts: list
    _last_reached_start: object | None
    _last_algo: object | None

    def _handle_start(self, start: State, idx: int) -> None:
        """
        ========================================================================
         Per-start sub-search body. Subclass override.

         Called by both `_run()` and `extend()`. At call time,
         `self._all_starts` holds the FULL current start
         sequence (originals + every prior extend + the
         current batch); `idx` is `start`'s position in
         `self._all_starts`. The subclass uses `idx <
         len(self._all_starts) - 1` to decide whether to
         lazy-re-push (where applicable).

         After a successful expansion the subclass MUST set
         `self._last_reached_start = start` and
         `self._last_algo = <its sub-search algo>` so
         `extend()` can re-push on the next call. On a
         fast-path or unreachable result, set
         `self._last_reached_start = None`.
        ========================================================================
        """
        raise NotImplementedError

    def _repush_last_reached_start(self) -> None:
        """
        ========================================================================
         Re-push `self._last_reached_start` onto OPEN under
         its sub-search's `h`, then clear both
         `_last_reached_start` and `_last_algo`. No-op when
         `_last_reached_start is None`.

         For kxA*-flavored MOSPP this is structurally inert
         (no shared frontier); the contract still requires
         the method to exist.
        ========================================================================
        """
        raise NotImplementedError

    # ──────────────────────────────────────────────────
    #  Public API
    # ──────────────────────────────────────────────────

    def extend(self,
               new_starts: list[State]) -> SolutionMOSPP:
        """
        ========================================================================
         Resume the orchestrator with additional starts
         appended to the sequence solved by `run()` (and any
         prior `extend()`s).

         Returns a `SolutionMOSPP` over the FULL set of starts
         seen so far (across `run()` + every `extend()`).

         Preconditions:
           - `run()` has completed at least once (else
             `RuntimeError`).
           - `new_starts` is non-empty (else `ValueError`).
           - Caller is responsible for the prefix-extending
             contract; duplicate starts are handled by the
             orchestrator's existing fast-paths (e.g.,
             AStarRepMOSPP's `already_reached`).
        ========================================================================
        """
        if self._elapsed is None:
            raise RuntimeError(
                'extend() requires a completed run() first')
        if not new_starts:
            raise ValueError('new_starts must be non-empty')

        # Start the call's wall-clock and re-anchor the phase
        # timer.
        t0 = perf_counter()
        if self._is_timing:
            self._t_phase_start = t0
        self._phase = PHASE_SEARCH

        # Re-push the previous run/extend's last completed
        # start (inert for kxA*-flavored MOSPP).
        self._repush_last_reached_start()

        # Append the new starts to the full sequence and run
        # the loop at the offset.
        offset = len(self._all_starts)
        self._all_starts.extend(new_starts)
        for j, start in enumerate(new_starts):
            self._handle_start(start, idx=offset + j)

        # Post: flush phase bucket, accumulate elapsed,
        # re-sync frontier counters + memory snapshot, then
        # finalize `mem_total = Σ mem_*` LAST — mirrors
        # `AlgoMOSPP._run_post` so `extend()` leaves the
        # counters in the same consistent state as `run()`.
        # Without the finalize, `mem_total` stays stale at
        # its last-`run()` value after an extend.
        from f_hs.algo.u_mem import finalize_mem_total
        self._flush_phase_timer()
        self._elapsed = (self._elapsed or 0.0) + (
            perf_counter() - t0)
        self._sync_frontier_counters()
        self._sync_memory_snapshot()
        finalize_mem_total(self._counters)
        return SolutionMOSPP(self._solutions)

    @classmethod
    def run_nested(cls,
                   problems: list,
                   h: Callable,
                   name: str | None = None,
                   is_recording: bool = False,
                   is_timing: bool = True
                   ) -> 'ExtendableMOSPP':
        """
        ========================================================================
         Convenience: solve a prefix-extending sequence of
         MOSPP problems by chaining `run()` and `extend()`.

         All problems share the same goal. Each problem after
         the first must have a `starts` list that is a
         prefix-superset of the previous — only the
         genuinely new starts are passed to `extend()`.

         Returns the orchestrator instance after the full
         sequence completes.
        ========================================================================
        """
        kw = dict(h=h, is_recording=is_recording,
                  is_timing=is_timing)
        if name is not None:
            kw['name'] = name
        algo = cls(problems[0], **kw)
        algo.run()
        for p in problems[1:]:
            seen = set(algo._all_starts)
            new = [s for s in p.starts if s not in seen]
            if new:
                algo.extend(new)
        return algo


def is_extendable(algo: object) -> bool:
    """
    ============================================================================
     Capability check: does `algo` support `.extend(new_starts)`?

     Equivalent to `isinstance(algo, ExtendableMOSPP)`. The
     OMSPP-scope `is_extendable` checks `ExtendableOMSPP` —
     scope determines which mixin is queried.
    ============================================================================
    """
    return isinstance(algo, ExtendableMOSPP)
