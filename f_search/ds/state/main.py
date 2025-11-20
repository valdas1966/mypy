from f_core.mixins.has.key import HasKey, Key


class State(HasKey[Key]):
    """
    ============================================================================
     Configuration in a Search-Space.
    ============================================================================
    """

    # Factory
    Factory: type = None
    
    def __init__(self, key: Key) -> None:
        """
        ========================================================================
         Initialize the State.
        ========================================================================
        """
        HasKey.__init__(self, key=key)

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the State.
        ========================================================================
        """
        return f'State({self.key.row},{self.key.col})'
