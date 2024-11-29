from abc import ABC, abstractmethod


class ManagerBase(ABC):
    """
    ============================================================================
     Abstract-Class that manages some Process.
    ============================================================================
    """

    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        pass

