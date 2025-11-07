import os
from abc import ABC, abstractmethod


class File(ABC):
    """
    ============================================================================
     Base class for all file handlers with Open and Close functionality.
    ============================================================================
    """

    def __init__(self,
                 # Path to the file
                 path: str
                 ) -> None:
        """
        ========================================================================
         Initialize the file handler.
        ========================================================================
        """
        # Store the old_path to the file.
        self._path = path
        # Open the file.
        self._open()

    @property
    def path(self) -> str:
        """
        ========================================================================
         Get the old_path to the file.
        ========================================================================
        """
        return self._path

    @abstractmethod
    def close(self) -> None:
        """
        ========================================================================
         Close the file (must be implemented by subclasses).
        ========================================================================
        """
        pass

    @abstractmethod
    def _open(self) -> None:
        """
        ========================================================================
         Open the file (must be implemented by subclasses).
        ========================================================================
        """
        pass
   