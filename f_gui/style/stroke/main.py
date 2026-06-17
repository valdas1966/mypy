from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from f_color.rgb import RGB


class DashPattern(Enum):
    """
    ========================================================================
     Stroke dash pattern — shared by Line and by Border edges.
    ========================================================================
     Values are the exact CSS keywords (border-style / SVG dash family),
     so the renderer maps them with zero translation.
    ========================================================================
    """
    SOLID = 'solid'
    DASHED = 'dashed'
    DOTTED = 'dotted'


class Stroke:
    """
    ============================================================================
     Stroke — the visual appearance of a line (color, width, pattern).
    ============================================================================
     Pure appearance, no geometry. Reused as: the look of a `Line`
     (Line = Stroke + endpoints + arrow) and as a single edge of a
     `Border` (Border = up to four Strokes).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 color: RGB = RGB(name='Black'),
                 width: float = 1,
                 pattern: DashPattern = DashPattern.SOLID) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._color = color
        self._width = width
        self._pattern = pattern

    @property
    def color(self) -> RGB | None:
        """
        ========================================================================
         Get the Color of the Stroke (None = renderer default).
        ========================================================================
        """
        return self._color

    @property
    def width(self) -> float:
        """
        ========================================================================
         Get the Width of the Stroke (in pixels).
        ========================================================================
        """
        return self._width

    @property
    def pattern(self) -> DashPattern:
        """
        ========================================================================
         Get the dash Pattern of the Stroke (solid / dashed / dotted).
        ========================================================================
        """
        return self._pattern

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Stroke.
        ========================================================================
        """
        color = self._color if self._color is not None else 'default'
        return f'({self._width}px {self._pattern.value} {color})'
