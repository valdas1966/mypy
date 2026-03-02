from f_core.mixins.has.children.main import HasChildren


class Factory:
    """
    ============================================================================
     Factory for the HasChildren class.
    ============================================================================
    """

    @staticmethod
    def empty() -> HasChildren:
        """
        ========================================================================
         Return a HasChildren with no children.
        ========================================================================
        """
        return HasChildren()

    @staticmethod
    def with_two() -> HasChildren:
        """
        ========================================================================
         Return a HasChildren with two children.
        ========================================================================
        """
        parent = HasChildren()
        parent.add_child(child=HasChildren())
        parent.add_child(child=HasChildren())
        return parent
