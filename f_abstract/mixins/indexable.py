from f_abstract.mixins.iterable import Iterable
from abc import abstractmethod
from typing import TypeVar

Item = TypeVar('Item')


class Indexable(Iterable[Item]):
    """
    ============================================================================
     Mixin-Class for Objects with Index.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._index = -1

    @property
    def index(self) -> int:
        """
        ========================================================================
         Return the current Index.
        ========================================================================
        """
        return self._index

    @abstractmethod
    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return List of all Items.
        ========================================================================
        """
        pass

    def current(self) -> Item:
        """
        ========================================================================
         Return the current Item.
        ========================================================================
        """
        return self[self._index]

    def next(self) -> Item:
        """
        ========================================================================
         Promote the Index to the next Item and return it.
        ========================================================================
        """
        self._index += 1
        return self.current()

    def has_next(self) -> bool:
        """
        ========================================================================
         Return True if the Index is not the Last.
        ========================================================================
        """
        return self._index < len(self) - 1
