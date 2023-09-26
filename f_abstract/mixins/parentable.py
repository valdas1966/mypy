from __future__ import annotations


class Parentable:
    """
    ============================================================================
     Mixin that has a Parent and a List of Children of the same type.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. add_child(child: Parentable) -> None
           [*] Adds a Child.
        2. remove_child(child: Parentable) -> None
           [*] Removes a Child from the Children-List.
    ============================================================================
    """

    _parent: Parentable                 # Object's Parent
    _children: list[Parentable]         # Object's Children

    def __init__(self,
                 parent: Parentable = None) -> None:
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
    def parent(self) -> Parentable:
        return self._parent

    @parent.setter
    def parent(self, new_parent: Parentable) -> None:
        """
        ========================================================================
            1. Remove self from the old Parent children-list (if not is None).
            2. Set a new Parent.
            3. Add self to the new Parent children-list (if not is None).
        ========================================================================
        """
        if self._parent:
            self._parent.remove_child(self)
        self._parent = new_parent
        if self._parent:
            self._parent.add_child(self)

    @property
    def children(self) -> list[Parentable]:
        return self._children

    def add_child(self, child: Parentable) -> None:
        """
        ========================================================================
         Adds a new Child.
        ========================================================================
        """
        self._children.append(child)

    def remove_child(self, child: Parentable) -> None:
        """
        ========================================================================
         Removes a Child from the Children-List.
        ========================================================================
        """
        self._children.remove(child)
