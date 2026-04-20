from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HBase(Generic[State]):
    """
    ============================================================================
     Heuristic Source — abstract base.

     Three capabilities, orthogonal:
       1. __call__(state)      — h-value (required; default raises).
       2. is_perfect(state)    — h(state) == h*(state) (default False).
       3. suffix_next(state)   — next State on the optimal suffix
                                 to the goal (default None).

     Subclasses in Phase 1: HCallable (wrap a function), HCached
     (frozen dict of CacheEntry + goal). HBounded and pathmax are
     Phase 2 per 2026-04-20 session.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __call__(self, state: State) -> float:
        """
        ========================================================================
         Return h(state). Subclasses override.
        ========================================================================
        """
        raise NotImplementedError

    def is_perfect(self, state: State) -> bool:
        """
        ========================================================================
         Return True iff h(state) is known to equal h*(state).
         Default: never perfect.
        ========================================================================
        """
        return False

    def suffix_next(self, state: State) -> State | None:
        """
        ========================================================================
         Return the next State on the optimal suffix to the goal,
         or None when the suffix is unknown / state is the goal.
         Default: None.
        ========================================================================
        """
        return None

    def is_bounded(self, state: State) -> bool:
        """
        ========================================================================
         Return True iff h(state) was tightened by an admissible
         lower bound strictly greater than the underlying base h.
         Default: never bounded.

         Recording implication: AStar enriches push/pop events
         with `is_bounded=True` when this returns True. Consumers
         reading the event log can identify which states had their
         h improved by a HBounded-style bound.
        ========================================================================
        """
        return False
