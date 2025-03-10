from f_ds.nodes.i_1_parent import NodeParent as Node


class GenNodeParent:
    """
    ========================================================================
     Generate NodeParent objects.
    ========================================================================
    """

    @staticmethod
    def parent_child() -> tuple[Node, Node]:
        """
        ========================================================================
         Generate a tuple of parent and child nodes.
        ========================================================================
        """
        parent = Node(key='parent')
        child = Node(key='child', parent=parent)
        return parent, child
