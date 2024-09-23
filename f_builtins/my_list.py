from collections import UserList
from typing import Generic, TypeVar


Item = TypeVar('Item')


class MyList(list, Generic[Item]):
    """
    ============================================================================
     Custom List.
    ============================================================================
    """

    def move(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Move an Item to a given Index.
        ========================================================================
        """
        self.remove(item)
        self.insert(index, item)

    def replace(self, d: dict[Item, Item]) -> None:
        """
        ========================================================================
         Replace Items by a given Mapping.
        ========================================================================
        """
        for i, item in enumerate(self):
            if item in d:
                self[i] = d[item]
