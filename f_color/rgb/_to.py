from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_color.rgb.main import RGB


class To:
    """
    ============================================================================
     Conversion methods for RGB color.
    ============================================================================
    """

    def __init__(self, rgb: RGB) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._rgb = rgb

    def tuple(self,
              to_int: bool = False
              ) -> tuple[float, float, float]:
        """
        ========================================================================
         Return a Tuple-REPR of the RGB (used by matplotlib (floats)).
        ========================================================================
        """
        r, g, b = self._rgb._r, self._rgb._g, self._rgb._b
        if to_int:
            return int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    def hex(self) -> str:
        """
        ========================================================================
         Return a Hex-String of the RGB.
        ========================================================================
        """
        r, g, b = self.tuple(to_int=True)
        return f'#{r:02X}{g:02X}{b:02X}'

    def argb(self,
             alpha: int = 255
             ) -> str:
        """
        ========================================================================
         Return an ARGB-String of the RGB.
        ========================================================================
        """
        r, g, b = self.tuple(to_int=True)
        return f'{alpha:02X}{r:02X}{g:02X}{b:02X}'

    def ansi(self) -> str:
        """
        ========================================================================
         Return an ANSI 24-bit foreground escape code.
        ========================================================================
        """
        r, g, b = self.tuple(to_int=True)
        return f'\033[38;2;{r};{g};{b}m'
