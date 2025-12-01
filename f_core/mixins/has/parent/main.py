from __future__ import annotations


class HasParent:
    """
    ============================================================================
     Mixin for objects that have a parent.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self, parent: HasParent = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._parent = parent

    @property
    def parent(self) -> HasParent:
        """
        ========================================================================
         Return the parent of the object.
        ========================================================================
        """
        return self._parent

    def path_from_root(self) -> list[HasParent]:
        """
        ========================================================================
         Return the path from the root to the current object.
        ========================================================================
        """
        path: list[HasParent] = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
