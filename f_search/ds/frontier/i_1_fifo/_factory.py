from f_search.ds.frontier.i_1_fifo.main import FrontierFifo


class Factory:
    """
    ============================================================================
     Factory for creating Frontier objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> FrontierFifo:
        """
        ========================================================================
         Create a FrontierFifo object with the 'A', 'B', 'C' states.
        ========================================================================
        """
        frontier = FrontierFifo[str]()
        frontier.push(state='A')
        frontier.push(state='B')
        frontier.push(state='C')
        return frontier
