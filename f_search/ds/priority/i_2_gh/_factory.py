from f_search.ds.priority.i_2_gh.main import PriorityGH


class Factory:
    """
    ============================================================================
     Factory for the PriorityGH class.
    ============================================================================
    """

    @staticmethod
    def a() -> PriorityGH:
        """
        ========================================================================
         Create a new PriorityGH object with the key 'A'.
        ========================================================================
        """
        key = 'A'
        g = 1
        h = 2
        return PriorityGH(key=key, g=g, h=h)

    @staticmethod
    def b() -> PriorityGH:
        """
        ========================================================================
         Create a new PriorityGH object with the key 'B'.
        ========================================================================
        """
        key = 'B'
        g = 2
        h = 1
        return PriorityGH(key=key, g=g, h=h)

    @staticmethod
    def c() -> PriorityGH:
        """
        ========================================================================
         Create a new PriorityGH object with the key 'C'.
        ========================================================================
        """
        key = 'C'
        g = 1
        h = 3
        return PriorityGH(key=key, g=g, h=h)
