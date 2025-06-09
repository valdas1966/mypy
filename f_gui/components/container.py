from __future__ import annotations
from f_ds.nodes.i_2_hierarchy import NodeHierarchy
from f_gui.components.component import Component
from f_gui.geometry.geometry import Geometry


class Container(Component, NodeHierarchy):
    """
    ============================================================================
     A UI component that can contain children and manage layout.
    ============================================================================
    """

    def __init__(self,
                 key: str,                # Unique identifier for the component
                 parent: Component,       # Parent component
                 geometry: Geometry       # Layout geometry of the component
                 ) -> None:
        """
        ========================================================================
         Initialize the container.
        ========================================================================
        """
        NodeHierarchy.__init__(self, key=key, parent=parent)
        Component.__init__(self, key=key, parent=parent, geometry=geometry)
        

    def add_child(self, child: Component) -> None:
        NodeHierarchy.add_child(self, child)
        child.parent = self
        # optional: position child relative to self
        # child.geometry.parent = self.geometry.absolute

    def remove_child(self, key: str) -> Component:
        child = NodeHierarchy.remove_child(self, key=key)
        child.parent = None
        return child
