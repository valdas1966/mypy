
class Cacheable:
    """
    ============================================================================
     Mixin-Class for Objects that can be cached.
    ============================================================================
    """
    
    def __init__(self, is_cached: bool = None) -> None:
        self._is_cached = is_cached

    @property
    def is_cached(self) -> bool:
        """
        ========================================================================
         Return True if the object is cached.
        ========================================================================
        """
        return self._is_cached

    @is_cached.setter
    def is_cached(self, val: bool) -> None:
        """
        ========================================================================
         Set the cache status of the object.
        ========================================================================
        """
        self._is_cached = val

