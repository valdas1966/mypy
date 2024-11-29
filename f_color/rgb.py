from __future__ import annotations
from f_core.mixins.nameable import Nameable
import matplotlib.colors as mcolors


class RGB(Nameable):
    """
    ============================================================================
     RGB Color.
    ============================================================================
    """

    _CUSTOM = {'my_cyan': (0, 55, 110)}

    def __init__(self,
                 name: str = None,
                 r: float = None,
                 g: float = None,
                 b: float = None
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        if name:
            if name in RGB._CUSTOM:
                (r, g, b) = (x/255 for x in RGB._CUSTOM[name])
            else:
                (r, g, b) = mcolors.to_rgb(name)
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
        return cls(r=r/255, g=g/255, b=b/255)

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b

    def to_tuple(self) -> tuple[float, float, float]:
        """
        ========================================================================
         Return list Tuple-REPR of the RGB.
         Ex: (0.5, 0.0, 0.5)
        ========================================================================
        """
        return self._r, self._g, self._b

    def to_tuple_int(self) -> tuple[int, ...]:
        """
        ========================================================================
         Return an INT-Tuple REPR.
         Ex: (0, 255, 0)
        ========================================================================
        """
        return tuple(int(x*255) for x in self.to_tuple())

    def __str__(self) -> str:
        """
        ========================================================================
         Return list STR-REPR of the RGB.
         Ex: '(128, 0, 128)'
        ========================================================================
        """
        return str(self.to_tuple_int())
