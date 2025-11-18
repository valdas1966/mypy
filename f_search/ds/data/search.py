from f_search.ds.generated import Generated, State
from dataclasses import dataclass


@dataclass
class DataSearch:
    """
    ===========================================================================
     Data structure for search algorithms.
    ===========================================================================
    """
    # Priority Queue for Generated States
    generated: Generated
    # Set of Explored States
    explored: set[State]
    # Best current generated state
    best: State

