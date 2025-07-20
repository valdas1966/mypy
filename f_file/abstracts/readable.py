from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Output = TypeVar('Output')


class Readable(ABC, Generic[Output]):
    """
    ============================================================================
     Abstract class for all readable files.
    ============================================================================
    """
    
    @abstractmethod
    def read_all(self) -> Output:
        """
        ========================================================================
         Read the file.
        ========================================================================
        """
        pass
