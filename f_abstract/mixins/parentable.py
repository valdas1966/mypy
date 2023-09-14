from __future__ import annotations


class Parentable:
    """
    ============================================================================
     Desc: Object that has a Parent and a List of Children of the same type.
    ============================================================================
    """

    def __init__(self,
                 parent: Parentable = None,
                 children: list[Parentable] = list()) -> None:
        self._parent = parent
        self._children = children

    @property
    def parent(self) -> Parentable:
        return self._parent

    @parent.setter
    def parent(self, new_parent: Parentable) -> None:
        self._parent = new_parent

    @property
    def children(self) -> list[Parentable]:
        return self._children

    @children.setter
    def children(self, new_children: list[Parentable]) -> None:
        self._children = new_children
