from f_core.mixins.printable import Printable
from f_core.mixins.sizable import Sizable
from typing import Generic, TypeVar, Iterator, Union

K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


class Dictable(Generic[K, V], Printable, Sizable):
    """
    ========================================================================
     Abstract Base Class for dictionary-like objects.
    ========================================================================
    """

    def __init__(self, data: dict[K, V] = None) -> None:
        """
        ========================================================================
         Initialize the internal dictionary.
        ========================================================================
        """
        self._data: dict[K, V] = data or dict()

    def keys(self) -> list[K]:
        """
        ========================================================================
         Get the keys of the dictionary.
        ========================================================================
        """
        return list(self._data.keys())

    def values(self) -> list[V]:
        """
        ========================================================================
         Get the values of the dictionary.
        ========================================================================
        """
        return list(self._data.values())
    
    def get(self, key: K, default: V = None) -> V:
        """
        ========================================================================
         Get an item by key.
        ========================================================================
        """
        return self._data.get(key, default)
    
    def update(self, data: Union[dict[K, V], 'Dictable[K, V]']) -> None:
        """
        ========================================================================
         Update the internal dictionary with the given data.
        ========================================================================
        """
        if isinstance(data, dict):
            self._data.update(data)
        else:
            self._data.update(data._data)

    def __getitem__(self, key: K) -> V:
        """
        ========================================================================
         Get an item by key.
        ========================================================================
        """
        return self._data[key]
    
    def __setitem__(self, key: K, value: V) -> None:
        """
        ========================================================================
         Set an item by key.
        ========================================================================
        """
        self._data[key] = value

    def __contains__(self, key: K) -> bool:
        """
        ========================================================================
         Check if a key exists in the dictionary.
        ========================================================================
        """
        return key in self._data

    def __len__(self) -> int:
        """
        ========================================================================
         Return the length of the dictionary.
        ========================================================================
        """
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        """
        ========================================================================
         Make the class iterable by returning an iterator over keys.
        ========================================================================
        """
        return iter(self._data)

    def __str__(self) -> str:
        """
        ========================================================================
         String representation of the dictionary.
        ========================================================================
        """
        return str(self._data)

    def __eq__(self, other: 'Dictable[K, V]') -> bool:
        """
        ========================================================================
         Check if the two dictionaries are equal.
        ========================================================================
        """
        return self._data == other._data
