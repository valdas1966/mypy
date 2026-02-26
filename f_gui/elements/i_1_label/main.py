from f_gui.elements.i_0_base.main import Element
from f_ds.geometry.bounds import Bounds


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
                 name: str = 'Label') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Element.__init__(self, bounds=bounds, name=name)
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
