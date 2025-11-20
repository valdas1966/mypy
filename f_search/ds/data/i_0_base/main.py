from f_search.ds.generated import Generated
from f_search.ds import State, Cost


class DataSearch:
    """
    ===========================================================================
     Data structure for search algorithms.
    ===========================================================================
    """
    
    def __init__(self) -> None:
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
