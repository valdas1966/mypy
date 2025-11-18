from dataclasses import dataclass
from f_search.ds.cost import Cost, State


@dataclass
class DataState:
    """
    ===========================================================================
     Data structure for states.
    ===========================================================================
    """
    # Mapping of State's G-Values
    g: dict[State, int]
    # Mapping of State's H-Values
    h: dict[State, int]
    # Mapping of State's Total-Costs
    cost: dict[State, Cost]
    # Mapping of State's Parent
    parent: dict[State, State]
