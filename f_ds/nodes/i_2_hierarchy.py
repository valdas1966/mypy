from f_ds.nodes.i_1_parent import NodeParent, Key
from f_ds.nodes.i_1_children import NodeChildren
from typing import TypeVar

Node = TypeVar('Node', bound='NodeHierarchy')


class NodeHierarchy(NodeParent[Key], NodeChildren[Key]):
    """ 
    ============================================================================
     A node with a hierarchy.
    ============================================================================
    """

    def __init__(self,
                 key: Key,
                 parent: Node = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the Node.
        ========================================================================
        """
        NodeParent.__init__(self, key=key, parent=parent, name=name)
        NodeChildren.__init__(self, key=key, name=name)

    def add_child(self, child: Node) -> None:
        """
        ========================================================================
         Add a child to the object and set the child's parent to self.
        ========================================================================
        """
        NodeChildren.add_child(self, child=child)
        child.parent = self

    def remove_child(self, child: Node = None, key: Key = None) -> Node:
        """
        ========================================================================
         Remove a child from the object and set the child's parent to None.
         Can remove by child or key.
        ========================================================================
        """
        # If child is provided, use child's key.
        if child:
            key = child.key
        child = NodeChildren.remove_child(self, key=key)
        child.parent = None
        return child

    def _update_parent(self) -> None:
        """
        ========================================================================
         Additional updates when the parent is set.
         Add self to the parent's children if it is not already there.
        ========================================================================
        """
        if self not in self.parent.children:
            self.parent.add_child(child=self)
