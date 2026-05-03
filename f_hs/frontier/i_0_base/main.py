from f_core.counters.main import Counters
from typing import Any, Generic, Iterator, TypeVar

State = TypeVar('State')


class FrontierBase(Generic[State]):
    """
    ============================================================================
     Abstract Base for a Search Frontier.
     Holds candidate States awaiting expansion. Narrow interface:
     push, pop, decrease, contains, bool, len, iter, clear.

     Owns an always-on `f_core.counters.Counters` with three
     names — `cnt_push`, `cnt_pop`, `cnt_decrease` — initialized
     here so every concrete frontier exposes the same surface
     via the `counters` property. Subclasses are responsible for
     incrementing inside their concrete `push` / `pop` /
     `decrease` overrides where the operation actually occurs
     (FIFO ignores `decrease`, so it does not increment
     `cnt_decrease`; counts reflect what the frontier actually
     did, not what was called).
    ============================================================================
    """

    _COUNTER_NAMES: tuple[str, ...] = (
        'cnt_push', 'cnt_pop', 'cnt_decrease',
    )

    def __init__(self) -> None:
        """
        ========================================================================
         Init the heap-op counter scaffold. Subclasses MUST call
         `FrontierBase.__init__(self)` from their own `__init__`.
        ========================================================================
        """
        self._counters: Counters = Counters(
            names=self._COUNTER_NAMES)

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
