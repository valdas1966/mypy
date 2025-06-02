from typing import Generic, TypeVar
from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable

T = TypeVar('T', int, float)


class Bounds(Generic[T], Printable, Comparable):
    """
    ============================================================================
     1. Component Class to store Bounds values (Top, Left, Width, Height).
     2. It is used to store the bounding box of the GUI-Component.
     3. Example: bounds = Bounds(top=10, left=10, width=40, height=40)
    ============================================================================
    """

    def __init__(self,
                 top: T = None,
                 left: T = None,
                 width: T = None,
                 height: T = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._top: T = top
        self._left: T = left
        self._width: T = width
        self._height: T = height

    @property
    def top(self) -> T:
        """
        ========================================================================
         Get the Top value of the bounding box.
        ========================================================================
        """
        return self._top

    @property
    def left(self) -> T:
        """
        ========================================================================
         Get the Left value of the bounding box.
        ========================================================================
        """
        return self._left

    @property
    def width(self) -> T:
        """
        ========================================================================
         Get the Width value of the bounding box.
        ========================================================================
        """
        return self._width

    @property
    def height(self) -> T:
        """
        ========================================================================
         Get the Height value of the bounding box.
        ========================================================================
        """
        return self._height

    def to_tuple(self) -> tuple[T, T, T, T]:
        """
        ========================================================================
         Return the Top, Left, Width, Height values as a tuple.
        ========================================================================
        """
        return self.left, self.top, self.width, self.height

    def key_comparison(self) -> tuple[T, T, T, T]:
        """
        ========================================================================
         Compare by the object  Top-Width-Height values.
        ========================================================================
        """
        return self.to_tuple()

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(10, 20, 30, 40)'
        ========================================================================
        """
        return f'({self.top}, {self.left}, {self.width}, {self.height})'

