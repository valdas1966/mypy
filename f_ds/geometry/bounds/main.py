from typing import Generic, TypeVar

T = TypeVar('T', int, float)


class Bounds(Generic[T]): 
    """
    ========================================================================
     A named tuple representing the bounds of an object.
    ========================================================================
     Properties:
    ------------------------------------------------------------------------
        1. top: The top coordinate of the bounds.
        2. left: The left coordinate of the bounds.
        3. bottom: The bottom coordinate of the bounds.
        4. right: The right coordinate of the bounds.
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
        assert top <= bottom, f'Top must be less than bottom, got {top} > {bottom}'
        assert left <= right, f'Left must be less than right, got {left} > {right}'
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
        return self._top, self._left, self._bottom, self._right

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
        values = f'Top={self._top}, Left={self._left}, '
        values += f'Bottom={self._bottom}, Right={self._right}'
        return f'<{name}: {values}>'
