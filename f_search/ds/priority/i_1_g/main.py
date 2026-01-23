from f_search.ds.priority.i_0_key.main import PriorityKey, Key


class PriorityG(PriorityKey[Key]):
    """
    ============================================================================
     Priority based on the G-Value of a State.
    ============================================================================
    """

    # Factory
    def __init__(self, key: Key, g: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        PriorityKey.__init__(self, key=key)
        self._g = g

    def update(self, g: int) -> None:
        """
        ========================================================================
         Update the G-Value of the State.
        ========================================================================
        """
        self._g = g

    def key_comparison(self) -> tuple[int, Key]:
        """
        ========================================================================
         Return the Key of the State.
        ========================================================================
        """
        return -self._g, PriorityKey.key_comparison(self)
    
    def __repr__(self) -> str:
        """
        ========================================================================
         Return the string representation of the PriorityG.
        ========================================================================
        """
        return f'PriorityG(key={self._key}, g={self._g})'
