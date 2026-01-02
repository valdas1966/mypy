from f_core.mixins import Comparable
from typing import Generic, TypeVar

Key = TypeVar('Key')


class Cost(Generic[Key], Comparable):
    """
    ============================================================================
     Cost of a StateBase.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 key: Key,
                 g: int,
                 h: int,
                 is_cached: bool = False,
                 is_bounded: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key
        self._g = g
        self._h = h
        self._is_cached = is_cached
        self._is_bounded = is_bounded
        
    def key_comparison(self) -> tuple[int, int, int, int, Key]:
        """
        ========================================================================
         Return the StateBase's Cost.
        ========================================================================
        """
        return (self._g + self._h,
                int(not self._is_cached),
                int(not self._is_bounded),
                self._h,
                self._key)

    def __str__(self) -> str:
        """
        =======================================================================
         Return the State's Cost.
        =======================================================================
        """
        return str(self.key_comparison())
