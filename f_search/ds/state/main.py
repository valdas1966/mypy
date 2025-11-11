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
