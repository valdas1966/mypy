from f_abstract.mixins.printable import Printable
from f_abstract.components.ltwh import LTWH


class Position(Printable):
    """
    ============================================================================
     Component-Class to manage relative and absolute positions.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._relative = LTWH()
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
    def relative(self, val: tuple[int, int, int, int]) -> None:
        """
        ========================================================================
         Set the relative position (left, top, width, height).
        ========================================================================
        """
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
        self._parent = val
        ratio_width = int(val.width / self._relative.width)
        ratio_height = int(val.height / self._relative.height)
        left = val.left + ratio_width
        top = parent.top + ratio_height
        width = parent.width + ratio_width
        height = parent.height + ratio_height

    def update_absolute(self, parent: LTWH) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        ratio_width = int(parent.width / self._relative.width)
        ratio_height = int(parent.height / self._relative.height)
        self._absolute = LTWH()

        left = parent.left + ratio_width
        top = parent.top + ratio_height
        width = parent.width + ratio_width
        height = parent.height + ratio_height
        self._absolute = LTWH(left, top, width, height)

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '%(20,30,40,50) * (100x200) -> (20,60,40,100)'
        ========================================================================
        """
        str_relative = f'%{self._relative}'
        str_dimensions = f'({self._width_parent}x{self._height_parent})'
        return f'{str_relative} * {str_dimensions} -> {self.absolute}'
