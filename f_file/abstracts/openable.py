from abc import ABC, abstractmethod


class Openable(ABC):
    """
    ============================================================================
     Abstract class for all openable files.
    ============================================================================
    """

    @abstractmethod
    def open(self) -> None:
        """
        ========================================================================
         Open the file.
        ========================================================================
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """
        ========================================================================
         Close the file.
        ========================================================================
        """
        raise NotImplementedError
