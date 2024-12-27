
class HasDimensions:
    """
    ============================================================================
     Mixin for Objects that have Width and Height dimensions.
    ============================================================================
    """

    def __init__(self,
                 width: float = 100,
                 height: float = 100) -> None:
        """
        ========================================================================
         Initialize with specified width and height dimensions.
        ========================================================================
        """
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        """
        ========================================================================
         Get the width of the object.
        ========================================================================
        """
        return self._width

    @property
    def height(self) -> float:
        """
        ========================================================================
         Get the height of the object.
        ========================================================================
        """
        return self._height

    def __str__(self) -> str:
        """
        ========================================================================
         Returns string representation of dimensions tuple.
        ========================================================================
        """
        return f'({self.width}x{self.height})'
