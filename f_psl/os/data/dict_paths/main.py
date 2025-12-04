from f_psl.os.data.list_paths.main import ListPaths
from f_core.mixins.has.record import HasRecord
from collections import defaultdict


class DictPaths(defaultdict[str, ListPaths], HasRecord):
    """
    ============================================================================
     Dict of Paths.
    ============================================================================
    """

    RECORD_SPEC = {'domains': lambda o: len(o),
                   'paths': lambda o: sum(len(paths) for paths in o.values())}

    def __init__(self,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        defaultdict.__init__(self, lambda: ListPaths())
        HasRecord.__init__(self, name='DictPaths')
