from f_search.ds.data import DataBestFirst
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from f_search.ds.priority import PriorityGH
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataHeuristics(Generic[State], DataBestFirst[State]):
    """
    ===========================================================================
     Data structure for Heuristics.
    ===========================================================================
    """
    
    def __init__(self, frontier: FrontierPriority[State, PriorityGH]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataBestFirst.__init__(self, frontier=frontier)
        self.dict_h: dict[State, int] = dict()
