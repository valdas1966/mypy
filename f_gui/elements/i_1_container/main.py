from f_gui.elements.i_0_base.main import Element
from f_ds.geometry.bounds import Bounds


class Container(Element):
    """
    ========================================================================
     Container Element that can hold Children.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 bounds: Bounds[float] = None,
                 name: str = 'Container') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Element.__init__(self, bounds=bounds, name=name)
        self._children: list[Element] = list()

    @property
    def children(self) -> list[Element]:
        """
        ========================================================================
         Get the list of Children Elements.
        ========================================================================
        """
        return self._children

    def add(self, child: Element) -> None:
        """
        ========================================================================
         Add a Child Element to the Container.
        ========================================================================
        """
        child._parent = self
        self._children.append(child)
