from f_ds.nodes.mixins.has_parent import HasParent
from f_ds.nodes.mixins.has_children import HasChildren
from typing import Generic, TypeVar

K = TypeVar('K')
T = TypeVar('T', bound='HasHierarchy')


class HasHierarchy(Generic[K, T], HasParent[T], HasChildren[K, T]):
    """
    ============================================================================
     Mixin for objects that have a hierarchy (parent and children).
    ============================================================================
    """
    
    def __init__(self, parent: T = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasParent.__init__(self, parent=parent)
        HasChildren.__init__(self)

    def add_child(self, key: K, child: T) -> None:
        """
        ========================================================================
         Add a child to the object and set the child's parent to self.
        ========================================================================
        """
        HasChildren.add_child(self, key=key, child=child)
        child.parent = self

    def remove_child(self, key: K) -> None:
        """
        ========================================================================
         Remove a child from the object and set the child's parent to None.
        ========================================================================
        """
        child = HasChildren.remove_child(self, key=key)
        child.parent = None

    def _update_parent(self) -> None:
        """
        ========================================================================
         Add self to the parent's children if self is not already a child.
        ========================================================================
        """
        if self.parent and self not in self.parent.children():
            self.parent.add_child(key=self.key, child=self)
