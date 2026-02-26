from f_search.ds.state import StateBase
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataIncremental(Generic[State]):
    """
    ========================================================================
     Accumulated Heuristic Data for Backward Incremental Search.
    ========================================================================
     Stores exact distances (cached) and lower bounds (bounded) toward
      a shared goal, accumulated across multiple sub-searches.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 dict_cached: dict[State, int] = None,
                 dict_bounded: dict[State, int] = None) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self.dict_cached = dict_cached if dict_cached else dict()
        self.dict_bounded = dict_bounded if dict_bounded else dict()
