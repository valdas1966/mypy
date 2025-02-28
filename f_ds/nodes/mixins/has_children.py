from typing import Generic, TypeVar

T = TypeVar('T', bound='HasChildren')


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
        self._children: list[T] = []

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

    def set_children(self, children: list[T]) -> None:
        """
        ========================================================================
         Set the children of the object.
        ========================================================================
        """
        self._children = children

    def remove_child(self, child: T) -> None:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        self._children.remove(child)

    def clear_children(self) -> None:
        """
        ========================================================================
         Clear the children of the object.
        ========================================================================
        """
        self._children.clear()
