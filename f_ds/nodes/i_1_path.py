from __future__ import annotations
from f_ds.nodes.i_0_base import NodeBase


class NodePath(NodeBase):
    """
    ============================================================================
     Node in a Path.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 parent: NodePath = None) -> None:
        NodeBase.__init__(self, name)
        self._parent = parent

    @property
    # Node's Parent
    def parent(self) -> NodePath:
        return self._parent

    def update_parent(self, parent: NodePath) -> None:
        """
        ========================================================================
         Set a new Parent.
        ========================================================================
        """
        self._parent = parent

    def path_from_root(self) -> list[NodePath]:
        """
        ========================================================================
         Return the Path from the Start to the Current Node.
        ========================================================================
        """
        path = list()
        current = self
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]
