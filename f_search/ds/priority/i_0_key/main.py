from f_core.mixins.has import HasKey
from typing import TypeVar

Key = TypeVar('Key')


class PriorityKey(HasKey[Key]):
    """
    ============================================================================
     Priority based on the Key of a State.
    ============================================================================
    """
    pass
