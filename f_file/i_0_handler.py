import os
from abc import ABC, abstractmethod


class FileHandler(ABC):
    """
    ============================================================================
     Base class for all file handlers.
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
        # If the file does not exist, create it.
        if not os.path.exists(path):
            self._create()
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
    def save(self) -> None:
        """
        ========================================================================
         Save the file (must be implemented by subclasses).
        ========================================================================
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        ========================================================================
         Close the file (must be implemented by subclasses).
        ========================================================================
        """
        pass

    @abstractmethod
    def _create(self) -> None:
        """
        ========================================================================
         Create a new file (must be implemented by subclasses).
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
   
