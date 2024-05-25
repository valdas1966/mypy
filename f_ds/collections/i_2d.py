from f_ds.collections.i_1d import Collection1D
from f_abstract.mixins.has_row_col import HasRowCol
from f_abstract.mixins.has_rows_cols import HasRowsCols
from typing import TypeVar, Iterator

Item = TypeVar('Item', bound=HasRowCol)


class Collection2D(Collection1D[Item], HasRowsCols):
    """
    ============================================================================
     Abstract-Class represents a 2D-Collection of Items.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 items: list[list[Item]] = None,
                 rows: int = None,
                 cols: int = None
                 ) -> None:
        Collection1D.__init__(self, name=name, items=items)
        HasRowsCols.__init__(self, rows=rows, cols=cols)

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return a List of Items in the Collection.
        ========================================================================
        """
        return [item for row in self._items
                for item in row
                if item is not None]

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the Item is in the Collection.
        ========================================================================
        """
        return any(item in row for row in self._items)

    def __len__(self) -> int:
        """
        ========================================================================
         Return number of Items in the Collection.
        ========================================================================
        """
        return sum(len(row) for row in self._items)

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if the Collection is not Empty.
        ========================================================================
        """
        return bool(len(self))

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Collection.
         Ex: Name([...])
        ========================================================================
        """
        return f'{self.name}({self.to_list()})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return friendly REPR.
         Ex: <Collection1D: Name([...])>
        ========================================================================
        """
        return f'<{self.__class__.__name__}: {str(self)}>'

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iterating over the Items.
        ========================================================================
        """
        for row in self._items:
            for item in row:
                yield item
