from f_ds.nodes.mixins.has_children import HasChildren


class GenHasChildren:
    """
    ========================================================================
     Generator for HasChildren objects,
    ========================================================================
    """

    @staticmethod
    def two_childs() -> HasChildren:
        """
        ========================================================================
         Generate a HasChildren with two childs.
        ========================================================================
        """
        has_children = HasChildren[str, int]()
        has_children.add_child(key='left', child=1)
        has_children.add_child(key='right', child=2)
        return has_children
