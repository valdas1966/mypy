from typing import Generic, TypeVar
from f_abstract.mixins.printable import Printable

T = TypeVar('T')


class LTWH(Generic[T], Printable):
    """
    ============================================================================
    Component Class to store LTWH values (Left, Top, Width, Height).
    ============================================================================
    """

    def __init__(self,
                 left: T = None,
                 top: T = None,
                 width: T = None,
                 height: T = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    @property
    def left(self) -> T:
        return self._left

    @property
    def top(self) -> T:
        return self._top

    @property
    def width(self) -> T:
        return self._width

    @property
    def height(self) -> T:
        return self._height

    @property
    def values(self) -> tuple[T, T, T, T]:
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
        return f'({self.left}, {self.top}, {self.width}, {self.height})'
