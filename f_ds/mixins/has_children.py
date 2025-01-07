from f_core.mixins.has_name import HasName
from typing import Generic, TypeVar

T = TypeVar('T')


class HasChildren(Generic[T], HasName):
    """
    ============================================================================
     Mixin-Class for Objects with Children.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
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

    def remove_child(self, child: T) -> None:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        self._children.remove(child)
