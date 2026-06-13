from __future__ import annotations

from typing import TYPE_CHECKING

from f_gui.elements.i_0_element.main import Element
from f_ds.geometry.bounds import Bounds

if TYPE_CHECKING:
    from f_color.rgb import RGB
    from f_gui.style.border import Border
    from f_gui.style.text import TextStyle


class Label(Element):
    """
    ========================================================================
     Label Element (Leaf with Text).
    ========================================================================
     The text *content* is a plain `str`; its *appearance* (font, size,
     bold, color) is an optional `TextStyle` — separate, opt-in, exactly
     like `background` / `border`. `style=None` renders with the baseline
     default look (monospace, 12px).
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 bounds: Bounds[float] = None,
                 text: str = '',
                 name: str = 'Label',
                 background: RGB | None = None,
                 border: Border | None = None,
                 style: TextStyle | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Element.__init__(self, bounds=bounds, name=name,
                         background=background, border=border)
        self._text = text
        self._style = style

    @property
    def text(self) -> str:
        """
        ========================================================================
         Get the Text of the Label.
        ========================================================================
        """
        return self._text

    @property
    def style(self) -> TextStyle | None:
        """
        ========================================================================
         Get the TextStyle of the Label (None = renderer default look).
        ========================================================================
        """
        return self._style

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Label.
        ========================================================================
        """
        return f'{self.name}[{self._text}]{self._bounds}'
