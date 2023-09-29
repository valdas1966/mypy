from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.sortable import Sortable


class NameableAndSortable(Nameable, Sortable):
    """
    ============================================================================
     Mixin for Nameable and Sortable objects.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        Nameable.__init__(name=name)
        Sortable.__init__()
