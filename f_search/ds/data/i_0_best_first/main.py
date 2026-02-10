from f_search.ds.path import Path
from f_search.ds.state import StateBase
from f_search.ds.frontier import FrontierBase as Frontier
from typing import TypeVar, Callable, Generic

State = TypeVar('State', bound=StateBase)


class DataBestFirst(Generic[State]):
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
        self.explored = explored if explored else set()
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
