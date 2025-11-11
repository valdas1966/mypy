from f_search.ds.cost.main import Cost


class Factory:
    """
    ============================================================================
     Factory for creating costs.
    ============================================================================
    """

    @staticmethod
    def a() -> Cost[str]:
        """
        ========================================================================
         Create a new cost with the key 'A'.
        ========================================================================
        """
        return Cost[str](key='A', g=5, h=5, is_cached=True, is_bounded=True)
    
    @staticmethod
    def b() -> Cost[str]:
        """
        ========================================================================
         Create a new cost with the key 'B'.
        ========================================================================
        """
        return Cost[str](key='B', g=5, h=5, is_cached=True, is_bounded=False)
    
    @staticmethod
    def c() -> Cost[str]:
        """
        ========================================================================
         Create a new cost with the key 'C'.
        ========================================================================
        """
        return Cost[str](key='C', g=5, h=5, is_cached=False, is_bounded=False)
    
    @staticmethod
    def d() -> Cost[str]:
        """
        ========================================================================
         Create a new cost with the key 'D'.
        ========================================================================
        """
        return Cost[str](key='D', g=4, h=6, is_cached=False, is_bounded=False)
    
    @staticmethod
    def e() -> Cost[str]:
        """
        ========================================================================
         Create a new cost with the key 'E'.
        ========================================================================
        """
        return Cost[str](key='E', g=4, h=6, is_cached=False, is_bounded=False)
    