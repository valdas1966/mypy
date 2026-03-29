from f_search.ds.data import DataBestFirst
from f_search.ds.frontier import FrontierPriority
from f_search.ds.state import StateBase
from f_search.ds.priority import PriorityGH
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataHeuristicsVector(Generic[State], DataBestFirst[State]):
    """
    ============================================================================
     Data structure for Vector-based Heuristics (one h per goal).
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 frontier: FrontierPriority[State, PriorityGH],
                 explored: set[StateBase] = None,
                 dict_parent: dict[State, State] = None,
                 dict_g: dict[State, int] = None,
                 dict_h: dict[State, list[int]] = None) -> None:
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
        self.dict_h: dict[State, list[int]] = (dict_h if dict_h
                                                else dict())

    def data_state(self,
                   state: State,
                   h_agg: int = None) -> dict[str, any]:
        """
        ====================================================================
         Return a dict of State's stored Data (as key=value pairs).
        ====================================================================
        """
        data = super().data_state(state)
        g = data['g']
        h_vec = self.dict_h.get(state)
        data['h_vec'] = h_vec
        data['h'] = h_agg
        f = g + h_agg if g is not None and h_agg is not None else None
        data['f'] = f
        return data
