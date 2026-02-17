from __future__ import annotations
from typing import Self


class HasParent:
    """
    ============================================================================
     Mixin for objects that have a parent.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, parent: Self = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        assert isinstance(parent, Self), f'Parent must be an instance of {Self.__name__}, got {type(parent)}'
        self._parent = parent

    @property
    def parent(self) -> HasParent | None:
        """
        ========================================================================
         Return the parent of the object.
        ========================================================================
        """
        return self._parent

    def path_from_root(self) -> list[Self]:
        """
        ========================================================================
         Return the path from the root to the current object.
        ========================================================================
        """
        path: list[Self] = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
