from __future__ import annotations
from f_ds.nodes.i_2_hierarchy import NodeHierarchy
from f_gui.components.component import Component
from f_gui.layout.bounds import Bounds


class Container(NodeHierarchy):
    """
    ============================================================================
     A UI component that can contain children and manage layout.
    ============================================================================
    """

    def __init__(self,
                 key: str,  # Unique identifier for the component
                 parent: Component,  # Parent component
                 geometry: Bounds  # Layout layout of the component
                 ) -> None:
        """
        ========================================================================
         Initialize the container.
        ========================================================================
        """
        NodeHierarchy.__init__(self, key=key, parent=parent)        

    @NodeHierarchy.parent.setter
    def parent(self, parent: Component) -> None:
        NodeHierarchy.parent.fset(self, parent)
        self.geometry.parent = parent.bounds.absolute

    def add_child(self, child: Component) -> None:
        NodeHierarchy.add_child(self, child)
        child.parent = self
        # optional: position child relative to self
        # child.layout.parent = self.layout.absolute

    def remove_child(self, key: str) -> Component:
        child = NodeHierarchy.remove_child(self, key=key)
        child.parent = None
        return child
