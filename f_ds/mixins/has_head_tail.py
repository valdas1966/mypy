from typing import Generic, TypeVar


Head = TypeVar('Head')
Tail = TypeVar('Tail')


class HasHeadTail(Generic[Head, Tail]):
    """
    ============================================================================
     Mixin for Data Structures with a Head and Tail properties.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Initialize the Head and Tail properties.
        ========================================================================
        """
        self._head: Head = None
        self._tail: Tail = None

    @property
    def head(self) -> Head:
        """
        ========================================================================
         Get the head property.
        ========================================================================
        """
        return self._head

    @head.setter
    def head(self, value: Head) -> None:
        """
        ========================================================================
         Set the head property.
        ========================================================================
        """
        self._head = value

    @property
    def tail(self) -> Tail:
        """
        ========================================================================
         Get the tail property.
        ========================================================================
        """
        return self._tail

    @tail.setter
    def tail(self, value: Tail) -> None:
        """
        ========================================================================
         Set the tail property.
        ========================================================================
        """
        self._tail = value
