
class LTWH:
    """
    ============================================================================
     Component Class to store LTWH values (Left, Top, Width, Height).
    ============================================================================
    """

    def __init__(self,
                 left: int,
                 top: int,
                 width: int,
                 height: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._values = (left, top, width, height)

    @property
    def values(self) -> tuple[int, int, int, int]:
        """
        ========================================================================
         Return LTWH values.
        ========================================================================
        """
        return self._values

    @property
    def width(self) -> int:
        """
        ========================================================================
         Return the object's Width.
        ========================================================================
        """
        left, top, width, height = self.values
        return width - left

    @property
    def height(self) -> int:
        """
        ========================================================================
         Return the object's Height.
        ========================================================================
        """
        left, top, width, height = self.values
        return height - top
