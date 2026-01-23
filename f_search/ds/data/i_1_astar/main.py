from f_search.ds.data.i_0_best_first.main import DataBestFirst, Frontier
from f_search.ds.states.i_0_base.main import StateBase as State
from f_search.ds.priority import PriorityKey as Priority


class DataAStar(DataBestFirst):
    """
    ============================================================================
     Data structure for A* Algorithms.
    ============================================================================
    """
    
    def __init__(self,
                 frontier: Frontier = None,
                 type_frontier: type = Frontier,
                 explored: set[State] = None,
                 best: State = None,
                 dict_g: dict[State, int] = None,
                 dict_h: dict[State, int] = None,
                 dict_priority: dict[State, Priority] = None,
                 dict_parent: dict[State, State] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataBestFirst.__init__(self,
                               frontier=frontier,
                               type_frontier=type_frontier,
                               explored=explored,
                               best=best,
                               dict_g=dict_g,
                               dict_parent=dict_parent)
        # Mapping of States to their H-Values
        self.dict_h: dict[State, int] = dict_h if dict_h else dict()
        # Mapping of States to their Priority
        self.dict_priority: dict[State, Priority] = dict_priority if dict_priority else dict()
