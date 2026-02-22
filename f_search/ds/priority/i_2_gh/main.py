from f_search.ds.priority.i_1_g.main import PriorityG, Key


class PriorityGH(PriorityG[Key]):
    """
    ============================================================================
     Priority based on the G-Value and H-Value of a State.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, key: Key, g: int, h: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        PriorityG.__init__(self, key=key, g=g)
        self._h = h

    def update(self, g: int = None, h: int = None) -> None:
        """
        ========================================================================
         Update the G-Value and H-Value of the State.
        ========================================================================
        """
        if g is not None:
            self._g = g
        if h is not None:
            self._h = h

    @property
    def key(self) -> tuple[int, tuple[int, Key]]:
        """
        ========================================================================
         Return the Key of the State.
        ========================================================================
        """
        return self._g + self._h, -self._g, super().key

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the string representation of the PriorityGH.
        ========================================================================
        """
        key = f'key={self._key}'
        g = f'g={self._g}'
        h = f'h={self._h}'
        return f'<PriorityGH: {key}, {g}, {h}>'
