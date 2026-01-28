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
                 make_frontier: Callable[[], Frontier[State]]) -> None:
        self.frontier = make_frontier()
        self.explored: set[State] = set()
        self.best: State = None
        self.dict_g: dict[State, int] = dict()
        self.dict_parent: dict[State, State] = dict()
        
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
