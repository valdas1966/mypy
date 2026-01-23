from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.frontier import FrontierFifo
from f_search.ds.states.i_0_base.main import StateBase as State


class Factory:
    """
    ============================================================================
     Factory for creating DataBestFirst objects.
    ============================================================================
    """
    
    @staticmethod
    def abc() -> DataBestFirst:
        """
        ========================================================================
         Create a DataBestFirst object with the 'A', 'B', 'C' states.
        ========================================================================
        """
        state_a = State.Factory.a()
        state_b = State.Factory.b()
        state_c = State.Factory.c()
        dict_parent = {state_a: None, state_b: state_a, state_c: state_b}
        return DataBestFirst(type_frontier=FrontierFifo, dict_parent=dict_parent)
