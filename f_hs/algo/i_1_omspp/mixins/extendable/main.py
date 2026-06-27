from f_hs.algo.i_1_omspp.i_0_base.main import PHASE_SEARCH
from f_hs.solution.main import SolutionOMSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter
from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class ExtendableOMSPP(Generic[State], ABC):
    """
    ============================================================================
     Capability mixin: OMSPP orchestrator supports
     **prefix-extending** the goal sequence after `run()`
     completes.

     Composed by orchestrators whose `_run()` body is a
     per-goal sub-search loop (today: `KAStarInc`; future:
     `KBFS`, `KDijkstra`). Provides the shared
     `extend(new_goals)` body and the `run_nested(problems,
     h)` classmethod convenience. Subclasses provide two
     hooks:

       - `_handle_goal(goal, idx)` — per-goal sub-search body,
         shared between `_run()` and `extend()`.
       - `_repush_last_reached_goal()` — re-push the previous
         run/extend's last reached goal onto OPEN under its
         sub-search's `h` (it was skipped at that time as the
         "last goal"; under `extend()` it now has a consumer).

     The mixin assumes composition with `AlgoOMSPP` and reads
     `self._all_goals`, `self._solutions`, `self._counters`,
     `self._recorder`, `self._elapsed`, `self._is_timing`,
     `self._phase`, `self._t_phase_start`. It calls
     `self._flush_phase_timer()`, `self._sync_frontier_counters()`,
     and `self._sync_memory_snapshot()` defined on `AlgoOMSPP`.

     Why a mixin (not a method on `AlgoOMSPP`):

       1. **Honest API surface.** `KAStarAgg` does NOT compose
          this mixin — its single-loop, Φ-aggregated structure
          makes `extend()` non-trivial (active-set re-growth,
          Φ-mode-dependent soundness). Callers can check
          `isinstance(algo, ExtendableOMSPP)` or call the
          `is_extendable(algo)` helper; `KAStarAgg` honestly
          reports no `extend()`.
       2. **Codebase convention.** Per `CLAUDE.md`: "Prefer
          mixins over deep single inheritance. Mixins are
          adjectives." Precedent at
          `f_hs/algo/i_0_oospp/mixins/bpmx/`.
       3. **Future opt-in.** When AGG-extend semantics settle
          (or `KBFS` / `KDijkstra` grow `extend()` first),
          adding the mixin to a class's bases is the entire
          opt-in step.

     KAStarInc-specific bookkeeping the subclass MUST maintain
     for `extend()` to work:

       - `self._all_goals: list[State]` — the full goal
         sequence seen so far (set to
         `list(self.problem.goals)` at the top of `_run`;
         appended to by `extend`).
       - `self._last_reached_goal: State | None` — the goal
         most recently expanded by a sub-search (None when no
         goal expanded yet, or after the last expansion's
         re-push has been consumed by `extend()`).
       - `self._last_algo` — the sub-search algo instance
         whose `_push(state=...)` is used to re-push
         `_last_reached_goal` under that sub-search's `h`.

     `_handle_goal` updates `_last_reached_goal` and
     `_last_algo` on every successful expansion;
     `_repush_last_reached_goal` clears both after re-pushing.
    ============================================================================
    """

    # Type-hint declarations — concrete values set by the
    # subclass __init__ / _run. Listed here so static checkers
    # see the contract even though the mixin doesn't bind
    # them.
    _all_goals: list
    _last_reached_goal: object | None
    _last_algo: object | None

    @abstractmethod
    def _handle_goal(self, goal: State, idx: int) -> None:
        """
        ========================================================================
         Per-goal sub-search body. Subclass override.

         Called by both `_run()` (during run()) and the mixin's
         `extend()` (during extend()). At call time,
         `self._all_goals` holds the FULL current goal sequence
         (originals + every prior extend + the current batch);
         `idx` is `goal`'s position in `self._all_goals`. The
         subclass uses `idx < len(self._all_goals) - 1` to
         decide whether to lazy-re-push (non-last reaches
         re-push; last does not).

         After a successful expansion the subclass MUST set
         `self._last_reached_goal = goal` and `self._last_algo
         = <its sub-search algo>` so `extend()` can re-push on
         the next call. On a fast-path or unreachable result,
         set `self._last_reached_goal = None`.
        ========================================================================
        """
        raise NotImplementedError

    @abstractmethod
    def _repush_last_reached_goal(self) -> None:
        """
        ========================================================================
         Re-push `self._last_reached_goal` onto OPEN under its
         sub-search's `h`, using `self._last_algo._push`.
         No-op when `_last_reached_goal is None` (no expansion
         yet, or already cleared). After the push, MUST clear
         both `_last_reached_goal` and `_last_algo` so a
         subsequent `extend()` does not re-push the same state.

         The next `_handle_goal` call's transition refresh
         re-keys the just-re-pushed state under the new goal's
         `h`.
        ========================================================================
        """
        raise NotImplementedError

    # ──────────────────────────────────────────────────
    #  Public API
    # ──────────────────────────────────────────────────

    def extend(self,
               new_goals: list[State]) -> SolutionOMSPP:
        """
        ========================================================================
         Resume the orchestrator with additional goals appended
         to the sequence solved by `run()` (and any prior
         `extend()`s).

         Returns a `SolutionOMSPP` over the FULL set of goals
         seen so far (across `run()` + every `extend()`). Same
         Mapping protocol as the `run()` return.

         Preconditions:
           - `run()` has completed at least once (else
             `RuntimeError`).
           - `new_goals` is non-empty (else `ValueError`).
           - Caller is responsible for the prefix-extending
             contract; duplicate goals are handled by the
             orchestrator's existing fast-paths (e.g., Inc's
             `already_reached` / `already_closed`).

         Accumulates work into `self._counters`,
         `self._elapsed`, `self._t_search`, `self._t_update`,
         `self._recorder`, and `self._solutions`. The Mapping
         returned spans **all** goals.
        ========================================================================
        """
        if self._elapsed is None:
            raise RuntimeError(
                'extend() requires a completed run() first')
        if not new_goals:
            raise ValueError('new_goals must be non-empty')

        # Start the call's wall-clock and re-anchor the phase
        # timer — phases accumulate from this moment until the
        # post-flush at the bottom.
        t0 = perf_counter()
        if self._is_timing:
            self._t_phase_start = t0
        # Default phase at entry is SEARCH — the prior
        # run/extend ended with a flush leaving _phase at
        # whatever its final value was; force back to SEARCH
        # for a clean baseline (the first _handle_goal will
        # flip to UPDATE around the transition refresh).
        self._phase = PHASE_SEARCH

        # Re-push the previous run/extend's last reached goal
        # under its sub-search's h. The next _handle_goal's
        # transition refresh re-keys it.
        self._repush_last_reached_goal()

        # Append the new goals to the full sequence and run
        # the goal loop at the offset.
        offset = len(self._all_goals)
        self._all_goals.extend(new_goals)
        for j, goal in enumerate(new_goals):
            self._handle_goal(goal, idx=offset + j)

        # Post: flush the trailing phase bucket, accumulate
        # this call's wall-clock into self._elapsed, and
        # re-sync the frontier counters + memory snapshot so
        # `algo.counters` reflects cumulative work.
        self._flush_phase_timer()
        self._elapsed = (self._elapsed or 0.0) + (
            perf_counter() - t0)
        self._sync_frontier_counters()
        self._sync_memory_snapshot()
        return SolutionOMSPP(self._solutions)

    @classmethod
    def run_nested(cls,
                   problems: list,
                   h: Callable,
                   name: str | None = None,
                   is_recording: bool = False,
                   is_timing: bool = True
                   ) -> 'ExtendableOMSPP':
        """
        ========================================================================
         Convenience: solve a prefix-extending sequence of
         OMSPP problems by chaining `run()` and `extend()`.

         All problems share the same start. Each problem after
         the first must have a `goals` list that is a
         prefix-superset of the previous — only the genuinely
         new goals (the suffix beyond what's already in
         `self._all_goals`) are passed to `extend()`.

         Returns the orchestrator instance after the full
         sequence completes; the caller reads `algo.solutions`,
         `algo.counters`, `algo.elapsed`, etc.
        ========================================================================
        """
        kw = dict(h=h, is_recording=is_recording,
                  is_timing=is_timing)
        if name is not None:
            kw['name'] = name
        algo = cls(problems[0], **kw)
        algo.run()
        for p in problems[1:]:
            seen = set(algo._all_goals)
            new = [g for g in p.goals if g not in seen]
            if new:
                algo.extend(new)
        return algo


def is_extendable(algo: object) -> bool:
    """
    ============================================================================
     Capability check: does `algo` support `.extend(new_goals)`?

     Equivalent to `isinstance(algo, ExtendableOMSPP)`; provided
     as a free function for callers that prefer functional
     idioms in capability fork tables.
    ============================================================================
    """
    return isinstance(algo, ExtendableOMSPP)
