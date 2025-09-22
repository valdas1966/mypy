from f_ds.nodes import NodeParent
from typing import Self, Generic, TypeVar

Key = TypeVar('Key')


class NodeCost(Generic[Key], NodeParent[Key]):
    """
    ============================================================================
     NodeCost with G, H and F values.
    ============================================================================
    """

    # Factory
    Factory: type = None
    
    def __init__(self,
                 key: Key,
                 h: int = None,
                 name: str = 'NodeCost',
                 parent: Self = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeParent.__init__(self, key=key, name=name, parent=parent)
        self._h = h
        self._g = self._calc_g()

    @property
    def g(self) -> int:
        """
        ========================================================================
         Get the g-value.
        ========================================================================
        """
        return self._g

    @property
    def h(self) -> int:
        """
        ========================================================================
         Get the h-value.
        ========================================================================
        """
        return self._h
    
    def f(self) -> int:
        """
        ========================================================================
        ========================================================================
        """
        return self.g + self.h
    
    def key_comparison(self) -> tuple[int, int, Key]:
        """
        ========================================================================
         Return the f-value, h-value, and key.
        ========================================================================
        """
        return self.f(), self.h, self.key
         
    def _calc_g(self) -> int:
        """
        ========================================================================
         Calculate the g-value (by the parent's g-value).
        ========================================================================
        """
        if self.parent:
            return self.parent.g + 1
        else:
            return 0

    def _update_parent(self) -> None:
        """
        ========================================================================
         Recalculate the g-value (based on the new parent).
        ========================================================================
        """
        self._g = self._calc_g()
    