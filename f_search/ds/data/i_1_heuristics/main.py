from f_search.ds.data import DataBestFirst
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from f_search.ds.priority import PriorityGH
from f_search.heuristics import HeuristicsProtocol as Heuristics
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataHeuristics(Generic[State], DataBestFirst[State]):
    """
    ===========================================================================
     Data structure for Heuristics.
    ===========================================================================
    """

    # Factory
    Factory : type | None = None

    def __init__(self,
                 frontier: FrontierPriority[State, PriorityGH],
                 explored: set[StateBase] = None,
                 dict_parent: dict[State, State] = None,
                 dict_g: dict[State, int] = None,
                 dict_h: dict[State, int] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataBestFirst.__init__(self,
                               frontier=frontier,
                               explored=explored,
                               dict_parent=dict_parent,
                               dict_g=dict_g)
        self.dict_h = dict_h if dict_h else dict()

    def data_state(self, state: State) -> dict[str, any]:
        """
        ====================================================================
         Return a dict of State's stored Data (as key=value pairs).
        ====================================================================
        """
        data = super().data_state(state)
        h = self.dict_h.get(state)
        g = data['g']
        f = g + h if g is not None and h is not None else None
        data['f'] = f
        data['h'] = h
        return data
