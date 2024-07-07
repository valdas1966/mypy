from __future__ import annotations


class Parentable:
    """
    ============================================================================
     Mixin-Class for Objects with single Parent.
    ============================================================================
    """

    def __init__(self, parent: Parentable = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._parent = parent

    @property
    def parent(self) -> Parentable:
        return self._parent

    @parent.setter
    def parent(self, p: Parentable) -> None:
        self._parent = p

    def path_from_root(self) -> list[Parentable]:
        """
        ========================================================================
         Return the Path from the Start to the Current Node.
        ========================================================================
        """
        path = list()
        current = self
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]
