from f_core.mixins.has.name import HasName
from f_ds.geometry.bounds import Bounds


class Element(HasName):
    """
    ========================================================================
     Base-Class for all GUI Elements.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 bounds: Bounds[float] = None,
                 name: str = 'Element') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._bounds = bounds or Bounds.Factory.full()
        self._parent = None

    @property
    def bounds(self) -> Bounds[float]:
        """
        ========================================================================
         Get the Bounds of the Element (relative to Parent).
        ========================================================================
        """
        return self._bounds

    @property
    def parent(self) -> 'Element | None':
        """
        ========================================================================
         Get the Parent Element.
        ========================================================================
        """
        return self._parent

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Element.
        ========================================================================
        """
        return f'{self.name}{self._bounds}'
