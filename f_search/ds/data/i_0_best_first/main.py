from f_search.ds.path import Path
from f_search.ds.state import StateBase
from f_search.ds.data.mixins import HasDataState
from f_search.ds.frontier import FrontierBase as Frontier
from f_ds.set_ordered import SetOrdered
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataBestFirst(Generic[State], HasDataState[State]):
    """
    ===========================================================================
     Data structure for Best-First Algorithms.
    ===========================================================================
    """
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 frontier: Frontier[State],
                 explored: set[State] = None,
                 dict_g: dict[State, int] = None,
                 dict_parent: dict[State, State] = None) -> None:
        """
        =============================================================
         Init private Attributes.
        =============================================================
        """
        self.frontier = frontier
        self.explored = explored if explored else SetOrdered()
        self.dict_g = dict_g if dict_g else dict()
        self.dict_parent= dict_parent if dict_parent else dict()
        self.best: State | None = None

    def set_best_to_be_parent_of(self, state: State) -> None:
        """
        ========================================================================
         Set the Best-State to be the Parent of the given State.
        ========================================================================
        """
        self.dict_parent[state] = self.best
        self.dict_g[state] = self.dict_g[self.best] + 1 if self.best else 0
        
    def data_state(self, state: State) -> dict[str, any]:
        """
        ====================================================================
         Return a dict of State's stored Data (as key=value pairs).
        ====================================================================
        """
        data = super().data_state(state)
        data['g'] = self.dict_g.get(state)
        return data

    def list_explored(self) -> list[dict[str, any]]:
        """
        ========================================================================
         Return a list of dicts with stored Data for each explored State
          (in exploration order).
        ========================================================================
        """
        return [self.data_state(state=s) for s in self.explored]

    def path_to(self, state: State) -> Path:
        """
        ========================================================================
         Reconstruct the Path from Start to given State.
        ========================================================================
        """
        states: list[State] = list()
        cur = state
        while cur:
            states.append(cur)
            cur = self.dict_parent[cur]
        states = states[::-1]
        return Path(states=states)
