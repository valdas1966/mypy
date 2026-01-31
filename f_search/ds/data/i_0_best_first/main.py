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
    
    def __init__(self, frontier: Frontier[State]) -> None:
        self.frontier = frontier
        self.explored: set[State] = set()
        self.best: State = None
        self.dict_g: dict[State, int] = dict()
        self.dict_parent: dict[State, State] = dict()

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
