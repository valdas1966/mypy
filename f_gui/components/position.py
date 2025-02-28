from f_core.mixins.printable import Printable
from f_gui.components.ltwh import LTWH


class Position(Printable):
    """
    ============================================================================
     Component-Class to manage relative and absolute positions.
    ============================================================================
    """

    def __init__(self,
                 relative: tuple[float, float, float, float] | LTWH = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        if relative is None:
            relative = LTWH(top=0, left=0, width=100, height=100)
        elif type(relative) == tuple:
            relative = LTWH(*relative)
        self._relative = relative
        self._absolute = LTWH()
        self._parent = LTWH()

    @property
    def relative(self) -> LTWH:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._relative

    @relative.setter
    def relative(self, val: tuple[float, float, float, float] | LTWH) -> None:
        """
        ========================================================================
         Set the relative position (left, top, width, height).
        ========================================================================
        """
        if isinstance(val, LTWH):
            self._relative = val
        else:
            self._relative = LTWH(*val)

    @property
    def absolute(self) -> LTWH:
        """
        ========================================================================
         Get the absolute position (left, top, width, height).
        ========================================================================
        """
        return self._absolute

    @property
    def parent(self) -> LTWH:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: LTWH) -> None:
        """
        ========================================================================
         Set the parent's position.
        ========================================================================
        """
        self._parent = val
        self._update_absolute()

    def _update_absolute(self) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        left = int(self._parent.width * self._relative.left)
        top = int(self._parent.height * self._relative.top)
        width = int(self._parent.width * self._relative.width)
        height = int(self._parent.height * self._relative.height)
        self._absolute = LTWH(left, top, width, height)

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return f'{self.relative} X {self.parent} -> {self.absolute}'
