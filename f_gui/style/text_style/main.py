from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_color.rgb import RGB


class TextStyle:
    """
    ============================================================================
     TextStyle — the visual appearance of text (font, size, bold, color).
    ============================================================================
     Pure appearance, no content. The text *string* stays on the `Label`
     (its content); a `TextStyle` is the *presentation*, attached the same
     way `background` / `border` are — separate, opt-in, reusable across
     many Labels. Sits beside `Stroke` / `Border` in `f_gui.style`.
    ============================================================================
     The defaults reproduce the renderer's historical hard-coded text CSS
     (`monospace`, `12px`, not bold, no color -> inherits the page color),
     so a Label with no style renders byte-identically to before.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 font: str = 'monospace',
                 size: float = 12,
                 bold: bool = False,
                 color: RGB | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._font = font
        self._size = size
        self._bold = bold
        self._color = color

    @property
    def font(self) -> str:
        """
        ========================================================================
         Get the Font-Family of the Text (a CSS font-family value).
        ========================================================================
        """
        return self._font

    @property
    def size(self) -> float:
        """
        ========================================================================
         Get the Font-Size of the Text (in pixels).
        ========================================================================
        """
        return self._size

    @property
    def bold(self) -> bool:
        """
        ========================================================================
         Get whether the Text is Bold.
        ========================================================================
        """
        return self._bold

    @property
    def color(self) -> RGB | None:
        """
        ========================================================================
         Get the Color of the Text (None = inherit the page color).
        ========================================================================
        """
        return self._color

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the TextStyle.
        ========================================================================
        """
        weight = 'bold' if self._bold else 'normal'
        color = self._color if self._color is not None else 'default'
        return f'({self._font} {self._size}px {weight} {color})'
