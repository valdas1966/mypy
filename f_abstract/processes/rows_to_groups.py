from f_ds.groups.nested import NestedGroup, Group, Item
from abc import ABC, abstractmethod
from typing import Generic, Sequence


class RowsToGroups(ABC, Generic[Item]):
    """
    ============================================================================
     Abstract process of converting rows into NestedGroup.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._groups: NestedGroup[Item] | None = None
        self._group: Group[Item] | None = None

    def run(self,
            rows: Sequence[Sequence[str]],
            name: str = None) -> NestedGroup[Item]:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        self._groups = NestedGroup(name=name)
        for row in rows:
            self._process_row(row=row)
        self._finalize_group()
        return self._groups

    def _process_row(self, row: Sequence[str]) -> None:
        """
        ========================================================================
         Process a single Row.
        ========================================================================
        """
        if self._is_group_start(row=row):
            self._finalize_group()
            self._group = self._create_new_group(row=row)
        else:
            self._add_to_group(row=row)

    def _create_new_group(self, row: Sequence[str]) -> Group[Item]:
        """
        ========================================================================
         Return new Group with a name extracted from the Row.
        ========================================================================
        """
        name = self._extract_group_name(row=row)
        return Group(name=name)

    def _add_to_group(self, row: Sequence[str]) -> None:
        """
        ========================================================================
         Create an Item from Row and add it to the current Group.
        ========================================================================
        """
        item = self._create_item(row=row)
        self._group.append(item=item)

    def _finalize_group(self) -> None:
        """
        ========================================================================
         Finalize the group process by adding it into a NestedGroup.
        ========================================================================
        """
        if self._group:
            self._groups.append(self._group)

    @abstractmethod
    def _is_group_start(self, row: Sequence[str]) -> bool:
        """
        ========================================================================
         Return True if the Row indicates the start of a new Group.
        ========================================================================
        """
        pass

    @abstractmethod
    def _create_item(self, row: Sequence[str]) -> Item:
        """
        ========================================================================
         Return an Item created from the Row.
        ========================================================================
        """
        pass

    @abstractmethod
    def _extract_group_name(self, row: Sequence[str]) -> str:
        """
        ========================================================================
         Return a group name extracted from the Row.
        ========================================================================
        """
        pass
