
class Traversable:
    """
    ============================================================================
     Desc: Interface-Class with Traversability functionality.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. is_traversable : bool
    ============================================================================
    """

    def __init__(self, is_traversable: bool = True):
        self._is_traversable = is_traversable

    @property
    def is_traversable(self) -> bool:
        return self._is_traversable

    @is_traversable.setter
    def is_traversable(self, new_value: bool) -> None:
        self._is_traversable = new_value
