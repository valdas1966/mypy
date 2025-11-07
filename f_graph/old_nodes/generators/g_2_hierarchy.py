from f_graph.nodes.i_2_hierarchy import NodeHierarchy


class GenNodeHierarchy:
    """
    ========================================================================
     Generate NodeHierarchy objects.
    ========================================================================
    """

    @staticmethod
    def parent_child() -> tuple[NodeHierarchy, NodeHierarchy]:
        """
        ========================================================================
         Generate a parent and child NodeHierarchy.
        ========================================================================
        """
        parent = NodeHierarchy(key='parent')
        child = NodeHierarchy(key='child', parent=parent)
        return parent, child
