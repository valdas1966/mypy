from __future__ import annotations
from f_ds.nodes.i_1_parent import NodeParent
from f_gui.geometry.geometry import Geometry


class Component(NodeParent):
    """
    ============================================================================
     Base class for all UI components (visible or layout).
    ============================================================================
    """

    def __init__(self,
                 key: str,                # Unique identifier for the component
                 parent: Component,       # Parent component
                 geometry: Geometry       # Layout geometry of the component
                 ) -> None:
        """
        ========================================================================
         Initialize the component.
        ========================================================================
        """
        NodeParent.__init__(key=key, parent=parent)
        self._geometry = geometry
        self._geometry.parent = parent.geometry

    @property
    def geometry(self) -> Geometry:
        """
        ========================================================================
         Get the layout geometry of the component.
        ========================================================================
        """
        return self._geometry
    
    @NodeParent.parent.setter
    def parent(self, parent: Component) -> None:
        """
        ========================================================================
         Set the parent and update the geometry based on the parent's geo.
        ========================================================================
        """
        NodeParent.parent = parent
        self._geometry.parent = parent.geometry
