from f_ds.collections.i_1d import Collection1D, Item
from abc import ABC


class Collection2D(ABC, Collection1D[Item]):

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None
                 ) -> None:
        Collection1D.__init__(self, name=name)
        if not cols:
            col = row

