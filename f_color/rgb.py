from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
import matplotlib.colors as mcolors

class RGB(Nameable):
    """
    ============================================================================
     RGB Color.
    ============================================================================
    """

    _CUSTOM = {'my_cyan': (0, 55, 110)}

    def __init__(self,
                 r: float = None,
                 g: float = None,
                 b: float = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        if name:
            (r, g, b) = RGB._CUSTOM.get(name, mcolors.to_rgb(name))
        self._r, self._g, self._b = (r, g, b)

    @classmethod
    def from_int(cls,
                 r: int,
                 g: int,
                 b: int) -> RGB:
        """
        ========================================================================
         Init the RGB with values in the range 0-255.
        ========================================================================
        """
        return cls(r = r / 255.0,
                   g = g / 255.0,
                   b = b / 255.0)

    def to_tuple(self) -> tuple[float, float, float]:
        """
        ========================================================================
         Return a Tuple-REPR of the RGB.
         Ex: (0.5, 0, 0.5)
        ========================================================================
        """
        return (self._r, self._g, self._b)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-REPR of the RGB.
         Ex: '(128, 0, 128)'
        ========================================================================
        """
        t = tuple(int(x*255) for x in self.to_tuple())
        return str(t)
