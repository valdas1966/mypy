from f_search.ds.priority.i_1_g.main import PriorityG


class Factory:
    """
    ============================================================================
     Factory for the PriorityG class.
    ============================================================================
    """

    @staticmethod
    def a() -> PriorityG:
        """
        ========================================================================
         Create a new PriorityG object with the key 'A'.
        ========================================================================
        """
        key = 'A'
        g = 0
        return PriorityG(key=key, g=g)

    @staticmethod
    def b() -> PriorityG:
        """
        ========================================================================
         Create a new PriorityG object with the key 'B'.
        ========================================================================
        """
        key = 'B'
        g = 1
        return PriorityG(key=key, g=g)

    @staticmethod
    def c() -> PriorityG:
        """
        ========================================================================
         Create a new PriorityG object with the key 'C'.
        ========================================================================
        """
        key = 'C'
        g = 1
        return PriorityG(key=key, g=g)
