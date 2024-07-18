from typing import Generic, TypeVar

T = TypeVar('T')


class HasChildren(Generic[T]):
    """
    ============================================================================
     Mixin-Class for Objects with Children.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._children = list[T]()

    @property
    def children(self) -> list[T]:
        """
        ========================================================================
         Return object's children.
        ========================================================================
        """
        return self._children
