from __future__ import annotations
from f_ds.nodes.i_2_hierarchy import NodeHierarchy
from f_gui.geometry.geometry import Geometry


class Component(NodeHierarchy):
    """
    ============================================================================
     Base class for all UI components (visible or layout).
    ============================================================================
    """

    def __init__(self,
                 key: str,                   # Component's unique identifier
                 geometry: Geometry,         # Component's Layout geometry
                 parent: Component = None    # Parent component
                 ) -> None:
        """
        ========================================================================
         Initialize the component.
        ========================================================================
        """
        NodeHierarchy.__init__(self, key=key, parent=None)
        self._geometry = geometry
        if parent:
            self.parent = parent

    @property
    def geometry(self) -> Geometry:
        """
        ========================================================================
         Get the layout geometry of the component.
        ========================================================================
        """
        return self._geometry
    
    @NodeHierarchy.parent.setter
    def parent(self, new_parent: Component) -> None:
        """
        ========================================================================
         Set the parent and update the geometry based on the parent's geo.
        ========================================================================
        """
        NodeHierarchy.parent.__set__(self, new_parent)
        if new_parent:
            self._geometry.bounds_parent = new_parent.geometry.bounds_absolute
        # Update absolute bounds for each component's children
        for child in self.children:
            child.geometry.bounds_parent = self.geometry.bounds_absolute
