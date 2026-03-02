from f_gui.elements.i_0_element.main import Element
from f_core.mixins.has.children import HasChildren
from f_ds.geometry.bounds import Bounds


class Container(Element, HasChildren):
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
        HasChildren.__init__(self)

    def add_child(self, child: Element) -> None:
        """
        ========================================================================
         Add a Child Element to the Container.
        ========================================================================
        """
        child._parent = self
        HasChildren.add_child(self, child=child)
