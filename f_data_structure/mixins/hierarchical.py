from __future__ import annotations
from f_abstract.mixins.nameable import Nameable


class Hierarchical(Nameable):
    """
    ============================================================================
     1. Mixin that manages Parent-Children relationships.
     2. There can be only one Parent. When a new Parent is set, the Object
         removes automatically from the previous Parent's children-list.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. add_child(child: Hierarchical) -> None
           [*] Adds a Child.
        2. remove_child(child: Hierarchical) -> None
           [*] Removes a Child from the Children-List.
        3. path_from_ancestor(other: Hierarchical) -> List[Hierarchical]
           [*] Returns a Parent-Hierarchical Path from other Object to Current.
    ============================================================================
    """

    parent: Hierarchical                 # Object's Parent
    children: list[Hierarchical]         # Object's Children

    def __init__(self,
                 name: str = None,
                 parent: Hierarchical = None) -> None:
        """
        ========================================================================
         Inits the Attributes and adds self to the parent's children-list.
        ========================================================================
        """
        Nameable.__init__(self, name)
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)
        self._children = list()

    @property
    def parent(self) -> Hierarchical:
        return self._parent

    @parent.setter
    def parent(self, new_parent: Hierarchical) -> None:
        """
        ========================================================================
            1. Remove self from the old Parent children-list (if is not None).
            2. Set a new Parent.
            3. Add self to the new Parent's children-list (if is not None).
        ========================================================================
        """
        if self._parent:
            if self in self._parent.children:
                self._parent.remove_child(self)
        self._parent = new_parent
        if self._parent and self not in self._parent.children:
            self._parent.add_child(self)

    @property
    def children(self) -> list[Hierarchical]:
        return self._children

    def add_child(self, child: Hierarchical) -> None:
        """
        ========================================================================
         Adds a new Child.
        ========================================================================
        """
        self._children.append(child)
        if child.parent is not self:
            child.parent = self

    def remove_child(self, child: Hierarchical) -> None:
        """
        ================    ========================================================
         Removes a Child from the Children-List.
        ========================================================================
        """
        self._children.remove(child)
        if child.parent == self:
            child.parent = None

    def path_from_ancestor(self,
                           other: Hierarchical) -> list[Hierarchical]:
        """
        ========================================================================
         Returns a Parent-Hierarchy Path from a given Object to the Current.
        ========================================================================
        """
        if self == other:
            return [self]
        path = [self]
        current = self.parent
        while current and not current == other:
            path.append(current)
            current = current.parent
        # if the path is not found
        if not current:
            return None
        path.append(other)
        return path[::-1]
