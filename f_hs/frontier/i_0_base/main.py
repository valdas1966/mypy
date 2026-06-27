from f_core.counters.main import Counters
from typing import Any, Generic, Iterator, TypeVar

State = TypeVar('State')


class FrontierBase(Generic[State]):
    """
    ============================================================================
     Abstract Base for a Search Frontier.
     Holds candidate States awaiting expansion.
    ============================================================================
    """

    _COUNTER_NAMES: tuple[str, ...] = (
        'cnt_push', 'cnt_pop', 'cnt_decrease',
    )

    def __init__(self) -> None:
        """
        ========================================================================
         Init the heap-op counter scaffold and the lifetime
         high-water `_max_size`. Subclasses MUST call
         `FrontierBase.__init__(self)` from their own `__init__`,
         and MUST call `self._track_max_size()` at the end of
         every `push` override (after the actual insertion).
        ========================================================================
        """
        self._counters: Counters = Counters(
            names=self._COUNTER_NAMES)
        # Lifetime high-water mark of |frontier|. Updated by
        # subclass `push` via `_track_max_size()` after every
        # actual insertion. Survives `clear()` (peak is a
        # whole-run property; the OPEN region is non-monotone,
        # so the end-of-run `len()` understates the peak —
        # `max_size` is the principled "rule-2" reading).
        self._max_size: int = 0

    # ──────────────────────────────────────────────────
    #  Counters
    # ──────────────────────────────────────────────────

    @property
    def counters(self) -> Counters:
        """
        ========================================================================
         Always-on heap-op counters (`cnt_push`, `cnt_pop`,
         `cnt_decrease`). Survive `clear()`; reset only via a
         fresh frontier instance. The frontier is the single
         source of truth — upstream algorithms read these at
         end-of-run and may mirror into a wider scaffold via
         `Counters.assign`.
        ========================================================================
        """
        return self._counters

    @property
    def max_size(self) -> int:
        """
        ========================================================================
         Lifetime high-water mark of `len(frontier)` across the
         whole run (peak number of states ever simultaneously
         on OPEN). The OPEN region is non-monotone (states
         enter via `push`, leave via `pop`), so end-of-run
         `len()` understates the peak — `max_size` is the
         principled peak reading for `mem_open` accounting
         (rule-2 in the `f_hs/algo` memory-counter
         classification).

         Survives `clear()`: a drain-and-rebuild
         (`AlgoSPP.refresh_priorities`) does not reset the
         peak — the lifetime high-water mark stays intact.
        ========================================================================
        """
        return self._max_size

    def _track_max_size(self) -> None:
        """
        ========================================================================
         Bump `_max_size` to `len(self)` if it grew. Called by
         each subclass's `push` AFTER the actual insertion.
         O(1); does NOT call `getsizeof` (per-push hot path).
         `pop` / `decrease` cannot increase the size, so they
         do not call this hook.
        ========================================================================
        """
        n = len(self)
        if n > self._max_size:
            self._max_size = n

    # ──────────────────────────────────────────────────
    #  Interface
    # ──────────────────────────────────────────────────

    def push(self,
             state: State,
             priority: Any = None) -> None:
        """
        ========================================================================
         Push a State into the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def pop(self) -> State:
        """
        ========================================================================
         Pop and return the next State from the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def decrease(self,
                 state: State,
                 priority: Any = None) -> None:
        """
        ========================================================================
         Update the Priority of a State already in the Frontier.
         Default: no-op (for unpriorityed frontiers — does NOT
         increment `cnt_decrease`).
        ========================================================================
        """
        pass

    def clear(self) -> None:
        """
        ========================================================================
         Remove all States from the Frontier. Does NOT reset
         the counters — they accumulate over the whole run.
        ========================================================================
        """
        raise NotImplementedError

    def __contains__(self, state: State) -> bool:
        """
        ========================================================================
         Return True if the State is in the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Frontier is not empty.
        ========================================================================
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of States in the Frontier.
        ========================================================================
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[State]:
        """
        ========================================================================
         Iterate over States currently in the Frontier. Order is
         implementation-defined. Enables `list(frontier)` and
         callers (e.g., `AlgoSPP.refresh_priorities`) that need
         to visit all pending states.
        ========================================================================
        """
        raise NotImplementedError
