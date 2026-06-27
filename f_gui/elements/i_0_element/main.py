from __future__ import annotations
from f_core.mixins import HasName, HasParent
from f_ds.geometry.bounds import Bounds
from f_color.rgb import RGB
from f_gui.style.border import Border
from f_ds.geometry.point import Point
from f_ds.geometry.side import Side
from abc import ABC


class Element(HasName, HasParent, ABC):
    """
    ========================================================================
     Abstract Base-Class for all GUI Elements.
    ========================================================================
    """

    def __init__(self,
                 bounds: Bounds[float] = None,
                 name: str = 'Element',
                 background: RGB | None = None,
                 border: Border | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasParent.__init__(self)
        self._bounds = bounds or Bounds.Factory.full()
        self._background = background
        self._border = border

    @property
    def bounds(self) -> Bounds[float]:
        """
        ========================================================================
         Get the Bounds of the Element (relative to Parent).
        ========================================================================
        """
        return self._bounds

    @property
    def background(self) -> RGB | None:
        """
        ========================================================================
         Get the background Color of the Element (None = transparent).
        ========================================================================
        """
        return self._background

    @property
    def border(self) -> Border | None:
        """
        ========================================================================
         Get the Border of the Element (None = no border).
        ========================================================================
        """
        return self._border

    def anchor(self, side: Side) -> Point:
        """
        ========================================================================
         A connection point of the Element — the mid-point of the given Side.
        ========================================================================
         The four anchors (TOP / RIGHT / BOTTOM / LEFT) are where a Connector
         attaches; delegated to the Element's Bounds. Reads `self.bounds` (the
         property) so subclasses that compute bounds dynamically stay correct.
        ========================================================================
        """
        return self.bounds.anchor(side=side)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Element.
        ========================================================================
        """
        return f'{self.name}{self._bounds}'
