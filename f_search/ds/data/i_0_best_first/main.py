from f_search.ds.path import Path
from f_search.ds.state import StateBase as State
from f_search.ds.frontier import FrontierBase as Frontier


class DataBestFirst:
    """
    ===========================================================================
     Data structure for Best-First Algorithms.
    ===========================================================================
    """
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 frontier: Frontier = None,
                 type_frontier: type = Frontier,
                 explored: set[State] = None,
                 best: State = None,
                 dict_g: dict[State, int] = None,
                 dict_parent: dict[State, State] = None) -> None:
        """
        =======================================================================
         Init private Attributes.
        =======================================================================
        """
        # Frontier of generated States
        self.frontier: Frontier = frontier if frontier else type_frontier()
        # Set of explored States
        self.explored: set[State] = explored if explored else set()
        # Best current state
        self.best: State = best
        # Mapping of States to their G-Values
        self.dict_g: dict[State, int] = dict_g if dict_g else dict()
        # Mapping of States to their Parent
        self.dict_parent: dict[State, State] = dict_parent if dict_parent else dict()  
        
        
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
