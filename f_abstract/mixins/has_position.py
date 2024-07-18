from f_abstract.components.position import Position


class HasPosition:
    """
    ============================================================================
     Mixin-Class for Object's with Position.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._position = Position()

    @property
    def position(self) -> Position:
        """
        ========================================================================
         Return object's Position.
        ========================================================================
        """
        return self._position
