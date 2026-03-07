from f_core.mixins.has.parent.main import HasParent


class Factory:
    """
    ============================================================================
     Factory for the HasParent class.
    ============================================================================
    """

    @staticmethod
    def parent() -> HasParent:
        """
        ========================================================================
         Return a HasParent object without a parent.
        ========================================================================
        """
        return HasParent()

    @staticmethod
    def child() -> HasParent:
        """
        ========================================================================
         Return a HasParent object without a parent.
        ========================================================================
        """
        parent = Factory.parent()
        return HasParent(parent=parent)
