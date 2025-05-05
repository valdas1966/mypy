from __future__ import annotations
from f_core.mixins.comparable import Comparable
from f_core.mixins.has_name import HasName
import matplotlib.colors as mcolors


class RGB(HasName, Comparable):
    """
    ============================================================================
     RGB Color (Red, Green, Blue).
     Used to represent colors in computer graphics.
     Formally defined as a tuple of three numbers (R, G, B).
     In Web, UI and Image files common values are 0-255.
     In Math and Programming, common values are 0-1.
    ============================================================================
    """

    # Custom Colors that are commonly used.
    _CUSTOM = {'MY_CYAN': (0, 55, 110),
               'LIGHT_RED': (200, 110, 110),
               'LIGHT_YELLOW': (220, 200, 110),
               'LIGHT_GREEN': (120, 190, 120),
               'MATTE_GREEN': (80, 160, 80),
               'MATTE_YELLOW': (200, 200, 100),
               'MATTE_RED': (180, 80, 80)}

    def __init__(self,
                 r: float = None,  # Red-Value (0-1)
                 g: float = None,  # Green-Value (0-1)
                 b: float = None,  # Blue-Value (0-1)
                 name: str = None  # Color-Name (from matplotlib or custom)
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Initialize the HasName Mixin.
        HasName.__init__(self, name=name)
        # If the name is a custom color, set the values accordingly.
        if name:
            if name in RGB._CUSTOM:
                (r, g, b) = (x/255 for x in RGB._CUSTOM[name])
            else:
                (r, g, b) = mcolors.to_rgb(name)
        # Set the private attributes (R, G, B).
        self._r, self._g, self._b = (r, g, b)

    @property
    def r(self) -> float:
        """
        ========================================================================
         Return the Red-Value (0-1).
        ========================================================================
        """
        return self._r

    @property
    def g(self) -> float:
        """
        ========================================================================
         Return the Green-Value (0-1).
        ========================================================================
        """
        return self._g

    @property
    def b(self) -> float:
        """
        ========================================================================
         Return the Blue-Value (0-1).
        ========================================================================
        """
        return self._b

    def to_tuple(self,
                 to_int: bool = False  # Convert to int-tuple
                ) -> tuple[float, float, float]:
        """
        ========================================================================
         Return a Tuple-REPR of the RGB (used by matplotlib (floats)).
        ========================================================================
         Ex: (0.5, 0.0, 0.5)
        ========================================================================
        """
        if to_int:
            r = int(self._r * 255)
            g = int(self._g * 255)
            b = int(self._b * 255)
            return r, g, b
        return self._r, self._g, self._b

    def key_comparison(self) -> tuple[float, float, float]:
        """
        ========================================================================
         Return a Tuple-REPR of the RGB.
        ========================================================================
        """
        return self.to_tuple()

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-REPR of the RGB.
         Ex: '(128, 0, 128)'
        ========================================================================
        """
        return str(self.to_tuple())
