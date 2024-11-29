from f_core.mixins.has_children import HasChildren
from typing import Generic, TypeVar

T = TypeVar('T', bound='Parentable')


class Parentable(Generic[T], HasChildren[T]):
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
        HasChildren.__init__(self)
        self._parent = parent

    @property
    def parent(self) -> T:
        return self._parent

    @parent.setter
    def parent(self, val: T) -> None:
        self._parent = val

    def path_from_start(self) -> list[T]:
        """
        ========================================================================
         Return the Path from the Start to the Current Node.
        ========================================================================
        """
        path = list()
        current = self
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]
