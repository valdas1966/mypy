from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_gui.style.stroke import Stroke


class Border:
    """
    ============================================================================
     Border — up to four edge Strokes around an Element's box.
    ============================================================================
     Each side (top / left / bottom / right) is an independent `Stroke`, or
     None for no edge on that side. A line and a border edge share the same
     appearance vocabulary (`Stroke`); a border simply groups four of them.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 top: Stroke | None = None,
                 left: Stroke | None = None,
                 bottom: Stroke | None = None,
                 right: Stroke | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    @property
    def top(self) -> Stroke | None:
        """
        ========================================================================
         Get the top edge Stroke (None = no top border).
        ========================================================================
        """
        return self._top

    @property
    def left(self) -> Stroke | None:
        """
        ========================================================================
         Get the left edge Stroke (None = no left border).
        ========================================================================
        """
        return self._left

    @property
    def bottom(self) -> Stroke | None:
        """
        ========================================================================
         Get the bottom edge Stroke (None = no bottom border).
        ========================================================================
        """
        return self._bottom

    @property
    def right(self) -> Stroke | None:
        """
        ========================================================================
         Get the right edge Stroke (None = no right border).
        ========================================================================
        """
        return self._right

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Border.
        ========================================================================
        """
        sides = (('T', self._top), ('L', self._left),
                 ('B', self._bottom), ('R', self._right))
        parts = [f'{tag}={s}' for tag, s in sides if s is not None]
        return f'Border[{", ".join(parts)}]' if parts else 'Border[]'
