from f_core.mixins.has_name import HasName
from typing import Generic, TypeVar

T = TypeVar('T', bound='HasParent')



class HasParent(Generic[T], HasName):
    """
    ============================================================================
     Mixin-Class for Objects with single Parent.
    ============================================================================
    """

    def __init__(self, parent: T = None, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self.parent = parent

    @property
    def parent(self) -> T:
        """
        ========================================================================
         Return the parent of the object.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: T) -> None:
        """
        ========================================================================
         Set the parent of the object.
        ========================================================================
        """
        self._parent = val
        self._update_parent()

    def path_from_root(self) -> list[T]:
        """
        ========================================================================
         Return the path from the root to the current node.
        ========================================================================
        """
        path: list[T] = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
    
    def path_from_node(self, node: T) -> list[T]:
        """
        ========================================================================
         Return the path from the given node to the current node.
        ========================================================================
        """
        path: list[T] = []
        current = self
        while current:
            path.append(current)
            if current == node:
                break
            current = current.parent
        if current == node:
            return path[::-1]
        return [] # node not found

    def _update_parent(self) -> None:
        """
        ========================================================================
         Additional updates when the parent is set.
        ========================================================================
        """
        pass
