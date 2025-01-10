from __future__ import annotations
from f_ds.nodes.i_1_hierarchy import NodeHierarchy, UID
from f_ds.mixins.cacheable import Cacheable


class NodePath(NodeHierarchy[UID], Cacheable):
    """
    ============================================================================
     Node with a Path functionality.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 parent: NodePath = None,
                 is_cached: bool = None,
                 h: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeHierarchy.__init__(self, uid=uid, parent=parent)
        Cacheable.__init__(self, is_cached=is_cached)
        self._g = 0 if not parent else parent.g + 1
        self._h = h

    @property
    def g(self) -> int:
        """
        ========================================================================
         Get the Path-Cost from the Start to this Node.
        ========================================================================
        """
        return self._g
    
    @property
    def h(self) -> int:
        """
        ========================================================================
         Get the Heuristic-Distance from this Node to the Goal.
        ========================================================================
        """
        return self._h
    
    @h.setter
    def h(self, h: int) -> None:
        """
        ========================================================================
         Set the Heuristic-Distance from this Node to the Goal.
        ========================================================================
        """
        self._h = h

    def f(self) -> int:
        """
        ========================================================================
         Return a Heuristic-Distance from Node to the Goal.
        ========================================================================
        """
        return (self.g + self.h) if self.h else -self.g

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare between Nodes by: F, H, UID.
        ========================================================================
        """
        return [self.f(), not self._is_cached, -self.g, self.uid]
    
    def is_better_parent(self, parent: NodePath) -> bool:
        """
        ========================================================================
         Check if the given parent g-value is better than the current parent.
        ========================================================================
        """
        return self.parent.g > parent.g
    
    def _update_parent(self) -> None:
        """
        ========================================================================
         Update the Path-Cost from the Start to this Node based on the parent.
        ========================================================================
        """
        self._g = self.parent.g + 1 if self.parent else 0

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Representation of the Node.
        ------------------------------------------------------------------------
         Ex: '<NodePath: (0,0), g=2, h=3, f=5>'
        ========================================================================
        """
        return f'uid={self.uid}, g={self.g}, h={self.h}, f={self.f()}'

    @classmethod
    def generate_zero(cls) -> NodePath:
        """
        ========================================================================
         Generate a Node with UID=0, H=0.
        ========================================================================
        """
        return cls[int](uid=0, h=0)
    