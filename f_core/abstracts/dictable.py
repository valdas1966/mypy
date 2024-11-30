from abc import ABC, abstractmethod


class Dictable(ABC):
    """
    ============================================================================
     ABC-Class for Objects that can be converted into a Dict.
    ============================================================================
    """

    @abstractmethod
    def to_dict(self) -> dict:
        """
        ========================================================================
         Convert the object into a Dict.
        ========================================================================
        """
