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
        self._relative: LTWH | None = None
        self._absolute: LTWH | None = None
        self._width_parent = None
        self._height_parent = None

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

    def update_absolute(self,
                        width_parent: int,
                        height_parent: int) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        self._width_parent = width_parent
        self._height_parent = height_parent
        rel_left, rel_top, rel_width, rel_height = self._relative.values
        abs_left = int((rel_left / 100) * width_parent)
        abs_top = int((rel_top / 100) * height_parent)
        abs_width = int((rel_width / 100) * width_parent)
        abs_height = int((rel_height / 100) * height_parent)
        self._absolute = (abs_left, abs_top, abs_width, abs_height)

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: (20%, 30%, 40%, 50%) * (100x200) = (20, 60, 40, 100)
        ========================================================================
        """
        str_relative = f'({', '.join((str(x) + '%' for x in self._relative))})'
        str_dimensions = f'({self._width_parent}x{self._height_parent})'
        return f'{str_relative} * {str_dimensions} -> {self.absolute}'
