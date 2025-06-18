from f_color.rgb import RGB
from f_const.u_enum import Thickness


class BorderSide:
    """
    ============================================================================
     A side of a border of a GUI component.
    ============================================================================
    """

    def __init__(self,
                 # Color of the border side
                 color: RGB = None,
                 # Thickness of the border side
                 thickness: Thickness = Thickness.THIN) -> None:
        """
        ========================================================================
         Initialize the BorderSide.
        ========================================================================
        """
        self._color = color
        self._thickness = thickness

    @property
    def color(self) -> RGB:
        """
        ========================================================================
         Get the color of the border side.
        ========================================================================
        """
        return self._color

    @color.setter
    def color(self, val: RGB) -> None:
        """
        ========================================================================
         Set the color of the border side.
        ========================================================================
        """
        self._color = val

    @property
    def thickness(self) -> Thickness:
        """
        ========================================================================
         Get the thickness of the border side.
        ========================================================================
        """
        return self._thickness

    @thickness.setter
    def thickness(self, val: Thickness) -> None:
        """
        ========================================================================
         Set the thickness of the border side.
        ========================================================================
        """
        self._thickness = val

