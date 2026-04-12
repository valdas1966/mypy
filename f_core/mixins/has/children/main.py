from __future__ import annotations
from typing import Self


class HasChildren:
    """
    ============================================================================
     Mixin for objects that have children.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._children: list[Self] = list()

    @property
    def children(self) -> list[Self]:
        """
        ========================================================================
         Return the list of children.
        ========================================================================
        """
        return self._children

    def add_child(self, child: Self) -> None:
        """
        ========================================================================
         Add a child.
        ========================================================================
        """
        self._children.append(child)

    def remove_child(self, child: Self) -> None:
        """
        ========================================================================
         Remove a child from the children list.
         Raises ValueError if the child is not present.
        ========================================================================
        """
        self._children.remove(child)
