
class HasCache:

    def __init__(self, is_cached: bool = False) -> None:
        """
        ====================================================================
         Init private attributes.
        ====================================================================
        """
        self._is_cached = is_cached

    @property
    def is_cached(self) -> bool:
        """
        ====================================================================
         Get the is_cached attribute.
        ====================================================================
        """
        return self._is_cached

    @is_cached.setter
    def is_cached(self, is_cached: bool) -> None:
        """
        ====================================================================
         Set the is_cached attribute.
        ====================================================================
        """
        self._is_cached = is_cached
