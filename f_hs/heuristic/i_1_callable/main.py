from f_hs.heuristic.i_0_base.main import HBase
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HCallable(Generic[State], HBase[State]):
    """
    ============================================================================
     Heuristic Source backed by a raw Callable[[State], float].

     Carries no perfection / suffix information — both defaults
     (False / None) are inherited from HBase. Exists so that
     AStar can take `h: HBase | Callable` uniformly; raw
     callables are auto-wrapped.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, fn: Callable[[State], float]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._fn = fn

    def __call__(self, state: State) -> float:
        """
        ========================================================================
         Return h(state) by delegating to the wrapped Callable.
        ========================================================================
        """
        return self._fn(state)
