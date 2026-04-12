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
         If the Child already has a Parent, detach it from the old Parent first.
        ========================================================================
        """
        # Detach from old parent (if any)
        old_parent = child.parent
        if old_parent is not None:
            if old_parent is self:
                return
            old_parent.remove_child(child=child)
        # Attach to this Container
        child._set_parent(parent=self)
        HasChildren.add_child(self, child=child)

    def remove_child(self, child: Element) -> None:
        """
        ========================================================================
         Remove a Child Element from the Container and clear its Parent.
        ========================================================================
        """
        HasChildren.remove_child(self, child=child)
        child._set_parent(parent=None)
