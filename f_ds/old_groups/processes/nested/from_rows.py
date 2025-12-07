from f_core.processes.i_2_io import ProcessIO
from f_ds.old_groups import NestedGroup, Group, Item
from abc import abstractmethod
from typing import Generic, Sequence
from dataclasses import dataclass


@dataclass
class Input:
    rows: Sequence[Sequence[str]] = None
    name: str = None


class ProcRowsToNested(Generic[Item],
                       ProcessIO[Input, NestedGroup[Item]]):
    """
    ============================================================================
     Abstract process of converting rows into NestedGroup.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = 'Process: Rows to Nested Group') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, name=name, _input=_input)
        self._groups: NestedGroup[Item] | None = None
        self._group: Group[Item] | None = None

    def run(self) -> NestedGroup[Item]:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        self._groups = NestedGroup(name=self._input.name)
        for row in self._input.rows:
            self._process_row(row=row)
        self._finalize_group()
        return self._groups

    def _process_row(self, row: Sequence[str]) -> None:
        """
        ========================================================================
         Process a one_to_one Row.
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
