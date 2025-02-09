from __future__ import annotations
from f_ds.nodes.i_0_uid import NodeUid, UID


class NodeParent(NodeUid[UID]):
    """
    ============================================================================
     A node with a parent.
    ============================================================================
    """

    def __init__(self,
                 uid: UID,
                 name: str = 'NodeParent',
                 parent: NodeParent[UID] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeUid.__init__(self, uid=uid, name=name)
        self._parent = parent

    @property
    def parent(self) -> NodeParent[UID]:   
        """
        ========================================================================
         Return the parent of the object.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: NodeParent[UID]) -> None:
        """
        ========================================================================
         Set the parent of the object.
        ========================================================================
        """
        self._parent = val
        self._update_parent()

    def path_from_root(self) -> list[NodeParent[UID]]:
        """
        ========================================================================
         Return the path from the root to the current node.
        ========================================================================
        """
        path: list[NodeParent[UID]] = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
    
    def path_from_node(self, node: NodeParent[UID]) -> list[NodeParent[UID]]:
        """
        ========================================================================
         Return the path from the given node to the current node.
        ========================================================================
        """
        path: list[NodeParent[UID]] = []
        current = self
        while current:
            path.append(current)
            if current == node:
                break
            current = current.parent
        if current == node:
            return path[::-1]
        return []  # node not found

    def _update_parent(self) -> None:
        """
        ========================================================================
         Additional updates when the parent is set.
        ========================================================================
        """
        pass
