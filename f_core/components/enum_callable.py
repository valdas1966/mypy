from enum import Enum
from typing import Generic, TypeVar

T = TypeVar('T')


class EnumCallable(Generic[T], Enum):
    """
    ============================================================================
     Enum of Callable-Types.
    ============================================================================
    """
    
    def __call__(self, *args, **kwargs) -> T:
        """
        ========================================================================
         Call the Enum-Value.
        ========================================================================
        """
        return self.value(*args, **kwargs)
