from f_hs.frontier.i_1_fifo.main import FrontierFIFO


class Factory:
    """
    ========================================================================
     Factory for FrontierFIFO test instances.
    ========================================================================
    """

    @staticmethod
    def empty() -> FrontierFIFO[str]:
        """
        ====================================================================
         Empty FrontierFIFO.
        ====================================================================
        """
        return FrontierFIFO[str]()

    @staticmethod
    def abc() -> FrontierFIFO[str]:
        """
        ====================================================================
         FrontierFIFO with A, B, C pushed in order.
        ====================================================================
        """
        f = FrontierFIFO[str]()
        f.push(state='A')
        f.push(state='B')
        f.push(state='C')
        return f
