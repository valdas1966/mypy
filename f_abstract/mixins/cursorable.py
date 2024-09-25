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
        self._data = list(data) if data is not None else list()
        self._cursor = 0

    @property
    def cursor(self) -> int:
        """
        ========================================================================
         Current Index of the Object.
        ========================================================================
        """
        return self._cursor

    def has_next(self) -> bool:
        """
        ========================================================================
         Return True if there is a next Item.
        ========================================================================
        """
        return self.cursor < len(self._data) - 1

    def next(self) -> Item:
        """
        ========================================================================
         Return the next Item and advance the Cursor.
        ========================================================================
        """
        self.advance()
        return self._data[self.cursor]

    def advance(self, times: int = 1) -> None:
        """
        ========================================================================
         Advance the Cursor.
        ========================================================================
        """
        self._cursor += times

    def reset(self) -> None:
        """
        ========================================================================
         Reset the Cursor to the beginning of the Object.
        ========================================================================
        """
        self._cursor = 0

    def __len__(self) -> int:
        """
        ========================================================================
         Return a Number of Items in the Object.
        ========================================================================
        """
        return len(self._data)
