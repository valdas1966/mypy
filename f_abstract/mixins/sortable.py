from __future__ import annotations


class Sortable:
    """
    ============================================================================
     Mixin for Sortable-Objects.
    ============================================================================
    """

    def __lt__(self, other: Sortable) -> bool:
        pass

    def __le__(self, other: Sortable) -> bool:
        pass

    def __eq__(self, other: Sortable) -> bool:
        pass

    def __ne__(self, other: Sortable) -> bool:
        pass

    def __gt__(self, other: Sortable) -> bool:
        pass

    def __ge__(self, other: Sortable) -> bool:
        pass
