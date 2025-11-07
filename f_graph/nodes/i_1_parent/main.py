from f_graph.nodes.i_0_key import NodeKey, Key
from typing import Self


class NodeParent(NodeKey[Key]):
    """
    ============================================================================
     A node with a parent.
    ============================================================================
    """

    # Factory
    Factory: type = None
    
    def __init__(self,
                 key: Key,
                 name: str = 'NodeParent',
                 parent: Self = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeKey.__init__(self, key=key, name=name)
        self.parent = parent
 
    @property
    def parent(self) -> Self:
        """
        ========================================================================
         Return the parent of the object.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: Self = None) -> None:
        """
        ========================================================================
         Set the parent of the object.
        ========================================================================
        """
        self._parent = val
        self._update_parent()

    def path_from_root(self) -> list[Self]:
        """
        ========================================================================
         Return the old_path from the root to the current node.
        ========================================================================
        """
        path: list[NodeParent[Key]] = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]

    def path_from_node(self, node: Self) -> list[Self]:
        """
        ========================================================================
         Return the old_path from the given node to the current node.
        ========================================================================
        """
        path: list[NodeParent[Key]] = []
        current = self
        while current:
            path.append(current)
            if current == node:
                break
            current = current.parent
        if current == node:
            return path[::-1]
        return [] # node not found

    def _update_parent(self) -> None:
        """
        ========================================================================
         Additional updates when the parent is set.
        ========================================================================
        """
        pass
