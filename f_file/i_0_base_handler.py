from abc import ABC


class BaseFileHandler(ABC):
    """
    ============================================================================
     Base class for all file handlers providing core functionality.
    ============================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Initialize the i_0_base file handler with a file old_path.
        ========================================================================
        """
        self._path = path

    @property
    def path(self) -> str:
        """
        ========================================================================
         Get the old_path to the file.
        ========================================================================
        """
        return self._path

    def __enter__(self):
        """
        ========================================================================
         Context manager entry.
        ========================================================================
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        ========================================================================
         Context manager exit - close file if closable.
        ========================================================================
        """
        if hasattr(self, 'close'):
            self.close()