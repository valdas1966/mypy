from typing import Generic, TypeVar

T = TypeVar('T')


class Parentable(Generic[T]):
    """
    ============================================================================
     Mixin-Class for Objects with single Parent.
    ============================================================================
    """

    def __init__(self, parent: T = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._parent = parent

    @property
    def parent(self) -> T:
        return self._parent

    @parent.setter
    def parent(self, T) -> None:
        self._parent = T
