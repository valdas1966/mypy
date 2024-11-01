from f_ds.groups.group import Group, Item
from typing import Sequence


class UGroup:
    """
    ============================================================================
     Group Utils-Class.
    ============================================================================
    """

    @staticmethod
    def union(name: str, groups: Sequence[Group[Item]]) -> Group[Item]:
        """
        ========================================================================
         Generate a Group by union sequence of groups.
        ========================================================================
        """
        group = Group(name=name)
        for g in groups:
            group += g.data
        return group
