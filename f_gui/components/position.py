from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.components.generators.g_tlwh import GenTLWH, TLWH


class Position(Printable, Comparable):
    """
    ============================================================================
     Component-Class to manage relative and absolute positions.
    ============================================================================
    """

    def __init__(self,
                 relative: tuple[float, float, float, float] | TLWH = GenTLWH.full(),
                 parent: tuple[float, float, float, float] | TLWH = GenTLWH.full(),
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Inits Absolute later by _update_absolute()
        self._absolute: TLWH = None
        # Inits Relative
        if isinstance(relative, tuple):
            self._relative = TLWH(*relative)
        else:
            self._relative = relative
        # Inits Parent
        if isinstance(parent, tuple):
            self.parent = TLWH(*parent)
        else:
            self.parent = parent

    @property
    def relative(self) -> TLWH:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._relative

    @relative.setter
    def relative(self, val: tuple[float, float, float, float] | TLWH) -> None:
        """
        ========================================================================
         Set the relative position (left, top, width, height).
        ========================================================================
        """
        if isinstance(val, TLWH):
            self._relative = val
        else:
            self._relative = TLWH(*val)

    @property
    def absolute(self) -> TLWH:
        """
        ========================================================================
         Get the absolute position (left, top, width, height).
        ========================================================================
        """
        return self._absolute

    @property
    def parent(self) -> TLWH:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: TLWH) -> None:
        """
        ========================================================================
         Set the parent's position.
        ========================================================================
        """
        self._parent = val
        self._update_absolute()

    def key_comparison(self) -> tuple[float, float, float, float]:
        """
        ========================================================================
         Return the key-comparison of the object.
        ========================================================================
        """
        return self.absolute.to_tuple()

    def _update_absolute(self) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        top = (self._parent.height * self._relative.top / 100) + self._parent.top
        left = (self._parent.width * self._relative.left / 100) + self._parent.left
        width = (self._parent.width * self._relative.width / 100)
        height = (self._parent.height * self._relative.height / 100)
        self._absolute = TLWH(top, left, width, height)

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return f'{self.relative} X {self.parent} -> {self.absolute}'
