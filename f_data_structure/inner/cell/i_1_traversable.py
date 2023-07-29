from f_data_structure.inner.cell.i_0_init import CellInit


class CellTraversable(CellInit):
    """
    ============================================================================
     Desc: Cell indicating whether it's traversable.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. is_traversable (bool) : Indicates if the Cell is Traversable.
    ============================================================================
    """

    def __init__(self,
                 x: int,
                 y: int,
                 name: str) -> None:
        super().__init__(x, y, name)
        self._is_traversable = True

    @property
    def is_traversable(self) -> bool:
        return self._is_traversable

    @is_traversable.setter
    def is_traversable(self, new_value: bool) -> None:
        self._is_traversable = new_value
