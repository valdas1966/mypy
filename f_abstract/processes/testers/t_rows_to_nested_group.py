from typing import Sequence
from f_ds.groups.processes.nested.from_rows import (RowsToNestedGroup,
                                                    NestedGroup, Group)


class C(RowsToNestedGroup):

    def _is_group_start(self, row: Sequence[str]) -> bool:
        return len(row) == 1

    def _create_item(self, row: Sequence[str]) -> str:
        return ''.join(row)

    def _extract_group_name(self, row: Sequence[str]) -> str:
        return row[0]


def test():
    g_a = Group(name='A', data=['aa'])
    g_b = Group(name='B', data=['bb'])
    nested_true = NestedGroup(name='NESTED', data=[g_a, g_b])
    rows = [['A'], ['a', 'a'], ['B'], ['b', 'b']]
    nested_test = C().run(name='NESTED', rows=rows)
    assert nested_test == nested_true
