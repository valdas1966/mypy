from f_search.ds.generated import Generated
from f_search.ds.cost import Cost, State


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
        generated: Generated = Generated()
        # Set of Explored States
        explored: set[State] = set()
        # Best current generated state
        best: State = None
        # Mapping of State's G-Values
        g: dict[State, int] = dict()
        # Mapping of State's H-Values
        h: dict[State, int] = dict()
        # Mapping of State's Total-Costs
        cost: dict[State, Cost] = dict()
        # Mapping of State's Parent
        parent: dict[State, State] = dict()
