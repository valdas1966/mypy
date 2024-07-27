from f_ds.collections.i_1d import Collection1D, Item
from f_abstract.mixins.has_rows_cols import HasRowsCols


class Collection2D(Collection1D[Item], HasRowsCols):
    """
    ============================================================================
     Abstract-Class represents a 2D-Collection of Items.
    ============================================================================
    """

    def __init__(self,
                 items: list[list[Item]],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Collection1D.__init__(self, name=name, items=items)
        HasRowsCols.__init__(self, rows=len(items), cols=len(items[0]))

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return a flattened list representation of the 2D Object.
        ========================================================================
        """
        return [item for row in self._items for item in row]

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object.
         Ex: 'Name(Row,Col)'
        ========================================================================
        """
        return f'{self.name}{self.shape()}'
