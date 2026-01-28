from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.frontier import FrontierFifo


class Factory:
    """
    ============================================================================
     Factory for creating DataBestFirst objects.
    ============================================================================
    """
    
    @staticmethod
    def empty() -> DataBestFirst:
        """
        ========================================================================
         Create a DataBestFirst object with an empty Frontier.
        ========================================================================
        """
        return DataBestFirst(make_frontier=FrontierFifo)
