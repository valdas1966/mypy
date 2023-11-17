from f_abstract.mixins.nameable import Nameable


class Node(Nameable):
    """
    ============================================================================
     Node with a Name.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        Nameable.__init__(self, name)
