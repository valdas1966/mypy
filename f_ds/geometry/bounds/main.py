from typing import Generic, TypeVar
from f_core.mixins import Equatable

T = TypeVar('T', bound=float)


class Bounds(Equatable, Generic[T]):
    """
    ========================================================================
     A named tuple representing the bounds of an object.
    ========================================================================
     Attributes:
        top: The top coordinate of the bounds.
        left: The left coordinate of the bounds.
        bottom: The bottom coordinate of the bounds.
        right: The right coordinate of the bounds.
    ========================================================================
    """
    
    # Factory
    Factory: type | None = None

    def __init__(self,
                 top: T,
                 left: T,
                 bottom: T,
                 right: T) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    @property
    def top(self) -> T:
        """
        ========================================================================
         Get the top coordinate of the bounds.
        ========================================================================
        """
        return self._top

    @property
    def left(self) -> T:
        """     
        ========================================================================
         Get the left coordinate of the bounds.
        ========================================================================
        """
        return self._left

    @property
    def bottom(self) -> T:
        """
        ========================================================================
         Get the bottom coordinate of the bounds.
        ========================================================================        
        """
        return self._bottom

    @property
    def right(self) -> T:
        """
        ========================================================================
         Get the right coordinate of the bounds.
        ========================================================================
        """
        return self._right

    def to_tuple(self) -> tuple[T, T, T, T]:
        """
        ========================================================================
         Return the bounds as a tuple.
        ========================================================================
        """
        return (self._top, self._left, self._bottom, self._right)

    def key(self) -> tuple[T, T, T, T]:
        """
        ========================================================================
         Return the key of the bounds.
        ========================================================================
        """
        return self.to_tuple()

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the bounds.
        ========================================================================
        """
        return f'({self._top}, {self._left}, {self._bottom}, {self._right})'

    def __repr__(self) -> str:
        """
        ========================================================================
        Return the repr representation of the bounds.
        ========================================================================
        """
        name = self.__class__.__name__
        values = f'top={self._top}, left={self._left}, '
        values += f'bottom={self._bottom}, right={self._right}'
        return f'<{name}: {values}>'
