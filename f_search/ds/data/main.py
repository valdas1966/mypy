from f_search.ds import Cost, Path, StateBase as State
from f_search.ds.generated import Generated


class DataSearch:
    """
    ===========================================================================
     Data structure for search algorithms.
    ===========================================================================
    """
    
    def __init__(self, cached: dict[State, int] = dict()) -> None:
        """
        =======================================================================
         Init private Attributes.
        =======================================================================
        """
        # Priority Queue for Generated States
        self.generated: Generated = Generated()
        # Set of Explored States
        self.explored: set[State] = set()
        # Best current generated state
        self.best: State = None
        # Mapping of State's G-Values
        self.g: dict[State, int] = dict()
        # Mapping of State's H-Values
        self.h: dict[State, int] = dict()
        # Mapping of State's Total-Costs
        self.cost: dict[State, Cost] = dict()
        # Mapping of State's Parent
        self.parent: dict[State, State] = dict()
        # Mapping of State's Cached-Values (exact distance to goal)
        self.cached: dict[State, int] = cached
        # Mapping of State's Bounded-Values (more accurate distance to goal)
        self.bounded: dict[State, int] = dict()
        
    def path_to(self, state: State) -> Path:
        """
        ========================================================================
         Reconstruct the Path from Start to Best State.
        ========================================================================
        """
        states: list[State] = list()
        cur = state
        while cur:
            states.append(cur)
            cur = self.parent[cur]
        states = states[::-1]
        return Path(states=states)
