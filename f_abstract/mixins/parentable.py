from __future__ import annotations
from f_abstract.mixins.has_children import HasChildren


class Parentable(HasChildren):
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
        HasChildren.__init__(self)
        self._parent = parent

    @property
    def parent(self) -> Parentable:
        return self._parent

    @parent.setter
    def parent(self, val: Parentable) -> None:
        self._parent = val

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
