from __future__ import annotations

from typing import TYPE_CHECKING

from f_gui.elements.i_0_element.main import Element
from f_ds.geometry.bounds import Bounds

if TYPE_CHECKING:
    from f_color.rgb import RGB


class Label(Element):
    """
    ========================================================================
     Label Element (Leaf with Text).
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 bounds: Bounds[float] = None,
                 text: str = '',
                 name: str = 'Label',
                 background: RGB | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Element.__init__(self, bounds=bounds, name=name, background=background)
        self._text = text

    @property
    def text(self) -> str:
        """
        ========================================================================
         Get the Text of the Label.
        ========================================================================
        """
        return self._text

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Label.
        ========================================================================
        """
        return f'{self.name}[{self._text}]{self._bounds}'
