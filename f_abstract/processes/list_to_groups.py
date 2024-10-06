from abc import abstractmethod
from f_abstract.components.group import Group
from f_abstract.mixins.nameable import Nameable
from typing import Generic, TypeVar, Sequence

Item = TypeVar('Item')


class ABCListToGroups(Generic[Item], Nameable):

    def __init__(self,
                 data: list[Sequence[str]],
                 name: str = None) -> None:
        """
        Initialize the processor with a list of data rows.
        Each row is expected to be a sequence of strings (e.g., a list or a tuple).
        """
        Nameable.__init__(self, name=name)
        self.data = data  # Store the full list of data
        self.current_row: Sequence[str] | None = None
        self.current_group: Group[Item] | None = None

    def to_groups(self) -> Group[Group[Item]]:
        """
        Run the processor, looping through the rows and creating groups of items with a title.
        """
        groups: Group[Group[Item]] = Group(name=self.name)
        for row in self.data:
            self._process_row(row=row, groups=groups)
        # Append the final group
        if self.current_group:
            groups.append(self.current_group)
        return groups

    def _process_row(self,
                     row: Sequence[str],
                     groups: Group[Group[Item]]) -> None:
        if self._is_title(row=row):
            # Process the old Group before starting a new
            if self.current_group:
                groups.append(self.current_group)
            # Create a new Group
            name = self._get_group_name()
            self.current_group = Group(name=name)
        else:
            item = self.create_item()
            self.current_group.append(item)

    @abstractmethod
    def _is_title(self, row: Sequence[str]) -> bool:
        """
        Return True if the current row is a title row.
        """
        pass

    @abstractmethod
    def _get_group_name(self) -> str:
        pass

    @abstractmethod
    def create_item(self) -> str:
        pass
