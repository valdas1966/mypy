from typing import Type, TypeVar, Generic, Any
from enum import Enum

# Base-CLass of classes the Factory can create
T = TypeVar('T')


class Factory(Generic[T]):
    """
    ============================================================================
     Generic-Class for class creator.
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Initialize the Factory-Map with an empty registry.
        ========================================================================
        """
        self._map: dict[Enum, Type[T]] = dict()

    def register(self,
                 key: Enum,
                 cls: Type[T]) -> None:
        """
        ========================================================================
         Register a Class in the Factory-Map.
        ========================================================================
        """
        self._map[key] = cls

    def create(self,
               key: Enum,
               *args: Any,
               **kwargs: Any) -> T:
        """
        ========================================================================
         Create an Instance of the Registered-Class.
        ========================================================================
        """
        cls = self._map[key]
        return cls(*args, **kwargs)
