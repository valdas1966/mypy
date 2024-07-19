from f_abstract.mixins.printable import Printable


class LTWH(Printable):
    """
    ============================================================================
    Component Class to store LTWH values (Left, Top, Width, Height).
    ============================================================================
    """

    def __init__(self,
                 left: int = None,
                 top: int = None,
                 width: int = None,
                 height: int = None) -> None:
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def values(self) -> tuple[int, int, int, int]:
        """
        ========================================================================
         Return the Top, Left, Width, Height values.
        ========================================================================
        """
        return self.left, self.top, self.width, self.height

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(10,20,30,40)'
        ========================================================================
        """
        return f'({self.left},{self.top},{self.width},{self.height})'
