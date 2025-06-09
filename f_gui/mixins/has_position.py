from f_gui.geometry.geometry import Position


class HasPosition:
    """
    ============================================================================
     Mixin-Class for Object's with Position.
    ============================================================================
    """

    def __init__(self, position: Position = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._position = position if position else Position()

    @property
    def position(self) -> Position:
        """
        ========================================================================
         Return object's Position.
        ========================================================================
        """
        return self._position

    @position.setter
    def position(self, val: Position) -> None:
        """
        ========================================================================
         Set object's Position.
        ========================================================================
        """
        self._position = val
