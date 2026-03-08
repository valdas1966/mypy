from f_core.mixins.comparable import Comparable
from f_core.mixins.has.name import HasName
from f_color.rgb._to import To
from f_color.rgb._colors import _CUSTOM
import matplotlib.colors as mcolors


class RGB(HasName, Comparable):
    """
    ============================================================================
     RGB Color (Red, Green, Blue).
    ============================================================================
    """

    Factory: type = None
    From: type = None

    def __init__(self,
                 name: str | None = None,
                 r: float | None = None,
                 g: float | None = None,
                 b: float | None = None
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        if name:
            if name in _CUSTOM:
                (r, g, b) = (x/255 for x in _CUSTOM[name])
            else:
                (r, g, b) = mcolors.to_rgb(name)
        self._r, self._g, self._b = (r, g, b)
        self.to = To(rgb=self)

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

    @property
    def key(self) -> tuple[float, float, float]:
        """
        ========================================================================
         Return a Tuple-REPR of the RGB.
        ========================================================================
        """
        return self.to.tuple()

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-REPR of the RGB.
        ========================================================================
        """
        return str(self.to.tuple())
