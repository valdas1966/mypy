from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state.i_0_base.main import StateBase
from f_search.ds.priority import PriorityKey
from typing import TypeVar, Generic, Callable

State = TypeVar('State', bound=StateBase)
Priority = TypeVar('Priority', bound=PriorityKey)

class DataPriority(Generic[State, Priority], DataBestFirst[State]):
    """
    ============================================================================
     Data structure for A* Algorithms.
    ============================================================================
    """
    
    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        make_frontier = FrontierPriority[State, Priority]
        DataBestFirst.__init__(self, make_frontier=make_frontier)
        self.dict_h: dict[State, int] = dict()
        self.dict_priority: dict[State, Priority] = dict()
