from __future__ import annotations
from f_ds.nodes.i_0_key import NodeKey, Key
from typing import TypeVar

Node = TypeVar('Node', bound='NodeChildren')


class NodeChildren(NodeKey[Key]):
    """
    ============================================================================
     A node with children.
    ============================================================================
    """

    def __init__(self, key: Key, name: str = 'NodeChildren') -> None:
        """
        ========================================================================
         Initialize the NodeChildren.
        ========================================================================
        """
        NodeKey.__init__(self, key=key, name=name)
        self._children: dict[Key, Node] = dict()

    @property
    def children(self) -> dict[Key, Node]:
        """
        ========================================================================
         Return object's children.
        ========================================================================
        """
        return self._children

    def add_child(self, child: Node) -> None:
        """
        ========================================================================
         Add a child to the object.
        ========================================================================
        """
        self._children[child.key] = child

    def remove_child(self, key: Key) -> Node:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        return self._children.pop(key)

    def clear_children(self) -> None:
        """
        ========================================================================
         Clear the children of the object.
        ========================================================================
        """
        self._children.clear()
