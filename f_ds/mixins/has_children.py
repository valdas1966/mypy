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
    
    def add_child(self, child: T) -> None:
        """
        ========================================================================
         Add a child to the object.
        ========================================================================
        """
        self._children.append(child)

    def remove_child(self, child: T) -> None:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        self._children.remove(child)
