from typing import Generic, TypeVar
from f_abstract.mixins.printable import Printable
from f_abstract.mixins.comparable import Comparable

T = TypeVar('T', int, float)


class LTWH(Generic[T], Printable, Comparable):
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
        self._left: T = left
        self._top: T = top
        self._width: T = width
        self._height: T = height

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

    def to_tuple(self) -> tuple[T, T, T, T]:
        """
        ========================================================================
         Return the Top, Left, Width, Height values.
        ========================================================================
        """
        return self.left, self.top, self.width, self.height

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by the object Left-Top-Width-Height values.
        ========================================================================
        """
        return list(self.to_tuple())

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(10,20,30,40)'
        ========================================================================
        """
        return f'({self.left}, {self.top}, {self.width}, {self.height})'
