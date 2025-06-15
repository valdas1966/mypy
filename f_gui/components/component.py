from __future__ import annotations
from f_color.rgb import RGB
from f_ds.nodes.i_2_hierarchy import NodeHierarchy
from f_gui.layout.generators.g_bounds import GenBounds, Bounds


class Component(NodeHierarchy):
    """
    ============================================================================
     Base class for all UI components (visible or layout).
    ============================================================================
    """

    def __init__(self,
                 # Component's unique identifier
                 name: str,
                 # Component's Layout layout (default is full)
                 bounds: Bounds = GenBounds.full(),
                 # Parent component (default is None)
                 parent: Component = None,
                 # Component's background color (default is None)
                 background: RGB = None
                 ) -> None:
        """
        ========================================================================
         Initialize the component.
        ========================================================================
        """
        NodeHierarchy.__init__(self, key=name, name=name, parent=None)
        self._bounds = bounds
        self._background = background
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
    
    @property
    def background(self) -> RGB:
        """
        ========================================================================
         Get the background color of the component.
        ========================================================================
        """
        return self._background
    
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
