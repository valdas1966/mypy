from f_core.mixins.has.record import HasRecord
from collections import UserList


class ListPaths(UserList[str], HasRecord):
    """
    ============================================================================
     List of Paths.
    ============================================================================
    """

    RECORD_SPEC = {
        'paths': lambda o: len(o),
    }

    # Factory
    Factory = None

    def __init__(self,
                 paths: list[str] = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        paths = paths or []
        UserList.__init__(self, paths)
        HasRecord.__init__(self, name=name)
