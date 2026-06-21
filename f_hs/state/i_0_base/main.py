from f_core.mixins.has.key import HasKey
from typing import Generic, TypeVar

Key = TypeVar('Key')


class StateBase(Generic[Key], HasKey[Key]):
    """
    ============================================================================
     Configuration in a Search-Space.
    ============================================================================
    """

    def __init__(self, key: Key) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasKey.__init__(self, key=key)
