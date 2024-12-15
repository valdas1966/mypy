from f_ds.mixins.has_parent import HasParent
from typing import Generic, TypeVar

T = TypeVar('T', bound='HasG')


class HasG(Generic[T], HasParent[T]):
    """
    ============================================================================
     Mixin for Nodes with Parents and G-Values based on Parents.
    ============================================================================
    """

    def __init__(self, parent: T = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasParent.__init__(self, parent=parent)
        self._g = 0 if not parent else parent.g + 1

    @property
    def g(self) -> int:
        """
        ========================================================================
         Return the Path-Cost from the Start to the current Node.
        ========================================================================
        """
        return self._g

    @HasParent.parent.setter
    def parent(self, val: T) -> None:
        """
        ========================================================================
         Set a New-Parent and update the G-Value respectively.
        ========================================================================
        """
        HasParent.parent.fset(self, val)
        self._g = val.g + 1 if val else 0

    def is_better_parent(self, parent: T = None) -> bool:
        """
        ========================================================================
         Return True if the given Parent is better than the current.
        ========================================================================
        """
        if not parent:
            return False
        return not self._parent or self.g > parent.g + 1
