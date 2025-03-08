from f_ds.nodes.i_1_children import NodeChildren as Node


class GenNodeChildren:
    """
    ========================================================================
     Generate NodeChildren objects.
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
        child = Node(key='child')
        parent.add_child(child=child)
        return parent, child
