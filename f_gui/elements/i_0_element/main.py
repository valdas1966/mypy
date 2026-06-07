from __future__ import annotations

from typing import TYPE_CHECKING

from f_core.mixins.has.name import HasName
from f_core.mixins.has.parent import HasParent
from f_ds.geometry.bounds import Bounds

if TYPE_CHECKING:
    from f_color.rgb import RGB
    from f_gui.style.border import Border


class Element(HasName, HasParent):
    """
    ========================================================================
     Abstract Base-Class for all GUI Elements (not instantiable).
    ========================================================================
    """

    def __new__(cls, *args, **kwargs) -> 'Element':
        """
        ========================================================================
         Block direct instantiation — Element is abstract.
        ========================================================================
         Element provides bounds/name/parent for every GUI element but is
         never a usable leaf itself; create a concrete subclass instead.
        ========================================================================
        """
        if cls is Element:
            raise TypeError(
                'Element is abstract; instantiate a concrete subclass '
                '(Container, Label, Window).')
        return super().__new__(cls)

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

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Element.
        ========================================================================
        """
        return f'{self.name}{self._bounds}'
