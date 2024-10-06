from abc import abstractmethod
from f_abstract.components.group import Group
from f_abstract.mixins.nameable import Nameable
from typing import Generic, TypeVar, Sequence

Item = TypeVar('Item')


class ABCListToGroups(Generic[Item], Nameable):

    def __init__(self,
                 rows: list[Sequence[str]],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._rows = rows
        self._group: Group[Item] | None = None

    @staticmethod
    def to_groups(rows: list[Sequence[str]],
                  name: str = None) -> Group[Group[Item]]:
        """
        ========================================================================
         Convert the List of Rows into Nested-Group of Items.
        ========================================================================
        """
        groups: Group[Group[Item]] = Group(name=name)
        self._group = None
        for row in self._rows:
            self._process_row(row=row, groups=groups)
        # Append the final group
        if self._group:
            groups.append(self._group)
        return groups

    def _process_row(self,
                     row: Sequence[str],
                     groups: Group[Group[Item]]) -> None:
        if self._is_title(row=row):
            # Process the old Group before starting a new
            if self._group:
                groups.append(self._group)
            # Create a new Group
            name = self._get_group_name()
            self._group = Group(name=name)
        else:
            item = self.create_item()
            self._group.append(item)

    @abstractmethod
    def _is_title(self, row: Sequence[str]) -> bool:
        """
        ========================================================================
         Return True if the current row is a title row.
        ========================================================================
        """
        pass

    @abstractmethod
    def _get_group_name(self, row: Sequence[str]) -> str:
        """
        ========================================================================
         Extract a Group Name from the given Row.
        ========================================================================
        """
        pass

    @abstractmethod
    def create_item(self, row: Sequence[str]) -> Item:
        """
        ========================================================================
         Generate an Item from the given Row.
        ========================================================================
        """
        pass
