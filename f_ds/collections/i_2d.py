from f_ds.collections.i_1d import Collection1D, Item
from f_abstract.mixins.has_rows_cols import HasRowsCols
from typing import Iterator


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
        if items:
            rows = len(items)
            cols = len(items[0])
        HasRowsCols.__init__(self, rows=rows, cols=cols)

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
        return self.rows * self.cols

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable iterating over the Items.
        ========================================================================
        """
        for row in self._items:
            for item in row:
                yield item
