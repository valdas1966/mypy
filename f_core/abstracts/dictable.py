from f_core.mixins.printable import Printable
from typing import Generic, TypeVar

K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type

class Dictable(Printable,  Generic[K, V]):
    """
    ========================================================================
     Abstract Base Class for dictionary-like objects.
    ========================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Initialize the internal dictionary.
        ========================================================================
        """
        self._data: dict[K, V] = {}

    def __getitem__(self, key: K) -> V:
        """
        ========================================================================
         Get an item by key.
        ========================================================================
        """
        return self._data[key]

    def __contains__(self, key: K) -> bool:
        """
        ========================================================================
         Check if a key exists in the dictionary.
        ========================================================================
        """
        return key in self._data

    def __str__(self) -> str:
        """
        ========================================================================
         String representation of the dictionary.
        ========================================================================
        """
        return str(self._data)
