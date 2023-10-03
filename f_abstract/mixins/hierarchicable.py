from __future__ import annotations


class Hierarchicable:
    """
    ============================================================================
     1. Mixin that manages Parent-Children relationships.
     2. There can be only one Parent. When a new Parent is set, the Object
         removes automatically from the previous Parent's children-list.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. add_child(child: Parentable) -> None
           [*] Adds a Child.
        2. remove_child(child: Parentable) -> None
           [*] Removes a Child from the Children-List.
        3. path_from_ancestor(other: Hierarchicable) -> List[Hierarchicable]
           [*] Returns a Parent-Hierarchical Path from other Object to Current.
    ============================================================================
    """

    _parent: Hierarchicable                 # Object's Parent
    _children: list[Hierarchicable]         # Object's Children

    def __init__(self,
                 parent: Hierarchicable = None) -> None:
        """
        ========================================================================
         Inits the Attributes and adds self to the parent's children-list.
        ========================================================================
        """
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)
        self._children = list()

    @property
    def parent(self) -> Hierarchicable:
        return self._parent

    @parent.setter
    def parent(self, new_parent: Hierarchicable) -> None:
        """
        ========================================================================
            1. Remove self from the old Parent children-list (if is not None).
            2. Set a new Parent.
            3. Add self to the new Parent's children-list (if is not None).
        ========================================================================
        """
        if self._parent:
            self._parent.remove_child(self)
        self._parent = new_parent
        if self._parent:
            self._parent.add_child(self)

    @property
    def children(self) -> list[Hierarchicable]:
        return self._children

    def add_child(self, child: Hierarchicable) -> None:
        """
        ========================================================================
         Adds a new Child.
        ========================================================================
        """
        self._children.append(child)

    def remove_child(self, child: Hierarchicable) -> None:
        """
        ========================================================================
         Removes a Child from the Children-List.
        ========================================================================
        """
        self._children.remove(child)

    def path_from_ancestor(self,
                           other: Hierarchicable) -> list[Hierarchicable]:
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
            return list()
        path.append(other)
        return path[::-1]
