from f_core.mixins.has.key import HasKey, Key
from typing import Generic


class StateBase(Generic[Key], HasKey[Key]):
    """
    ============================================================================
     Configuration in a Search-Space.
    ============================================================================
    """

    # Factory
    Factory = None
    
    def __init__(self,
                 key: Key,
                 name: str = 'StateBase') -> None:
        """
        ========================================================================
         Initialize the StateBase.
        ========================================================================
        """
        HasKey.__init__(self, key=key, name=name)
