from typing import Generic, TypeVar, Iterable
from f_abstract.mixins.sizable import Sizable

Item = TypeVar('Item')


class Cursorable(Generic[Item], Sizable):
    """
    ============================================================================
     Mixin class for Cursor-Like functionality to any Iterable-Based class.
    ============================================================================
    """

    def __init__(self,
                 data: Iterable[Item] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._data: list[Item] = list(data) if data is not None else list()
        self._cursor = -1

    def cursor(self) -> int:
        """
        ========================================================================
         Current Index of the Object.
        ========================================================================
        """
        return self._cursor

    def current(self) -> Item:
        """
        ========================================================================
         Return the Current Item.
        ========================================================================
        """
        if self._cursor == -1:
            return None
        return self._data[self._cursor]

    def has_next(self) -> bool:
        """
        ========================================================================
         Return True if there is a next Item.
        ========================================================================
        """
        return self._cursor < len(self._data) - 1

    def has_prev(self) -> bool:
        """
        ========================================================================
         Return True if there is a previous Item.
        ========================================================================
        """
        return self._cursor >= 0

    def peek_next(self) -> Item:
        """
        ========================================================================
         Return the next Item.
        ========================================================================
        """
        return self._data[self._cursor + 1]

    def peek_prev(self) -> Item:
        """
        ========================================================================
         Return the previous Item.
        ========================================================================
        """
        return self._data[self._cursor - 1]

    def advance(self, times: int = 1) -> None:
        """
        ========================================================================
         Move cursor forward.
        ========================================================================
        """
        self._cursor += times

    def retreat(self, times: int = 1) -> None:
        """
        ========================================================================
         Move cursor back.
        ========================================================================
        """
        self._cursor -= times

    def prev(self) -> Item:
        """
        ========================================================================
         Mover cursor back and return the Item.
        ========================================================================
        """
        self.retreat()
        return self.current()

    def next(self) -> Item:
        """
        ========================================================================
         Move cursor forward and return the Item.
        ========================================================================
        """
        self.advance()
        return self.current()

    def reset(self) -> None:
        """
        ========================================================================
         Reset the Cursor to the beginning of the Object.
        ========================================================================
        """
        self._cursor = -1

    def __len__(self) -> int:
        """
        ========================================================================
         Return a Number of Items in the Object.
        ========================================================================
        """
        return len(self._data)

