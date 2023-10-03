from f_abstract.mixins.nameable import Nameable


class NodeNameable(Nameable):
    """
    ============================================================================
     Represents a simple Node with a Name.
    ============================================================================
    """

    # Nameable
    name: str       # Node's Name

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Initializes Node's Name.
        ========================================================================
        """
        Nameable.__init__(self, name)
