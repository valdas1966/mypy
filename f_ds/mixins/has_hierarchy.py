from __future__ import annotations
from f_ds.mixins.has_parent import HasParent
from f_ds.mixins.has_children import HasChildren
from typing import Generic, TypeVar

T = TypeVar('T', bound='HasHierarchy')


class HasHierarchy(Generic[T], HasParent[T], HasChildren[T]):
    """
    ============================================================================
     Mixin for objects that have a hierarchy (parent and children).
    ============================================================================
    """
    
    def __init__(self, parent: HasHierarchy = None, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasParent.__init__(self, parent=parent, name=name)
        HasChildren.__init__(self, name=name)

    def add_child(self, child: T) -> None:
        """
        ========================================================================
         Add a child to the object.
        ========================================================================
        """
        if child not in self.children():
            HasChildren.add_child(self, child=child)
            child.parent = self

    def remove_child(self, child: T) -> None:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        HasChildren.remove_child(self, child=child)
        child.parent = None

    def _update_parent(self) -> None:
        """
        ========================================================================
         Additional updates when the parent is set.
        ========================================================================
        """
        if self.parent and self not in self.parent.children():
            self.parent.add_child(self)
