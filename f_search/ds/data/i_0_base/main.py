from f_search.ds.generated import Generated
from f_search.ds import StateBase, Cost


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
        self.explored: set[StateBase] = set()
        # Best current generated state
        self.best: StateBase = None
        # Mapping of StateBase's G-Values
        self.g: dict[StateBase, int] = dict()
        # Mapping of StateBase's H-Values
        self.h: dict[StateBase, int] = dict()
        # Mapping of StateBase's Total-Costs
        self.cost: dict[StateBase, Cost] = dict()
        # Mapping of StateBase's Parent
        self.parent: dict[StateBase, StateBase] = dict()
