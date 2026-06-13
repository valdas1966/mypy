from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from f_color.rgb import RGB

# Sentinel: color not passed -> default to black. Resolved lazily in
# __init__ so f_color stays off TextStyle's module-load path. Pass an
# explicit `color=None` to opt OUT of a color (inherit the page color).
_DEFAULT_BLACK: Any = object()


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
     The default color is black (readable on a light background); the other
     defaults are `monospace`, `12px`, not bold. Pass `color=None` explicitly
     to opt OUT of a color and inherit the surrounding page color instead.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 font: str = 'monospace',
                 size: float = 12,
                 bold: bool = False,
                 color: RGB | None = _DEFAULT_BLACK) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
         `color` omitted -> black; `color=None` -> inherit the page color.
        ========================================================================
        """
        if color is _DEFAULT_BLACK:
            from f_color.rgb import RGB
            color = RGB('black')
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
        color = self._color if self._color is not None else 'inherit'
        return f'({self._font} {self._size}px {weight} {color})'
