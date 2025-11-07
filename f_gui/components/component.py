from __future__ import annotations
from f_color.rgb import RGB
from f_graph.nodes import NodeHierarchy
from f_gui.layout import FactoryBounds, Bounds
from f_gui.components.mixins.has_color import HasColor


class Component(NodeHierarchy, HasColor):
    """
    ============================================================================
     Base class for all UI components (visible or layout).
    ============================================================================
    """

    def __init__(self,
                 # Component's unique identifier
                 name: str,
                 # Component's Layout layout (default is full)
                 bounds: Bounds = FactoryBounds.full(),
                 # Parent component (default is None)
                 parent: Component = None,
                 # Component's background color (default is None)
                 color: RGB = None
                 ) -> None:
        """
        ========================================================================
         Initialize the component.
        ========================================================================
        """
        NodeHierarchy.__init__(self, key=name, name=name, parent=None)
        HasColor.__init__(self, color=color)
        self._bounds = bounds
        if parent:
            self.parent = parent

    @property
    def bounds(self) -> Bounds:
        """
        ========================================================================
         Get the layout layout of the component.
        ========================================================================
        """
        return self._bounds
    
    @NodeHierarchy.parent.setter
    def parent(self, new_parent: Component) -> None:
        """
        ========================================================================
         Set the parent and update the layout based on the parent's geo.
        ========================================================================
        """
        NodeHierarchy.parent.__set__(self, new_parent)
        if new_parent:
            self._bounds.parent = new_parent.bounds.absolute
        # Update absolute bounds for each component's children
        for child in self.children:
            child.bounds.bounds_parent = self.bounds.absolute
