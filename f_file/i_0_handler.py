import os
from abc import ABC, abstractmethod


class FileHandler(ABC):
    def __init__(self, path: str):
        self.path = path
        if os.path.exists(path):
            self._open()
        else:
            self._create()
            self._open()

    @abstractmethod
    def _open(self) -> None:
        """Open the file (must be implemented by subclasses)."""
        pass

    @abstractmethod
    def _create(self) -> None:
        """Create a new file (must be implemented by subclasses)."""
        pass
