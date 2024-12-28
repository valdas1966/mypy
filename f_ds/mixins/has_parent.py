from typing import Generic, TypeVar

T = TypeVar('T', bound='HasParent')



class HasParent(Generic[T]):
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
    def parent(self, val: T) -> None:
        self._parent = val

    def path_from(self, node: T = None) -> list[T]:
        """
        ========================================================================
         Return the Path from the given Node to the Current Node.
         If no node is provided, returns the path from root (node without parent).
        ========================================================================
        """
        if node and node == self:
            return [self]  # Special case: path is just the current node
        path = []
        current = self
        while current:
            path.append(current)
            if node and current == node:
                break
            current = current.parent
        return path[::-1] if node is None or current == node else []
