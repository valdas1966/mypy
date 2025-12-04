from collections import defaultdict
from f_core.mixins.has.record import HasRecord
from f_search.experiments.data.i_0_filepaths_maps import FilepathsMaps


class DomainFilepaths(defaultdict[str, FilepathsMaps], HasRecord):
    """
    ============================================================================
     DomainFilepaths is a dictionary of domain filepaths.
     The key is the domain and the value is a FilepathsMaps object.
    ============================================================================
    """

    RECORD_SPEC = {
        'filepaths': lambda o: sum(len(filepaths) for filepaths in o.values()),
        'domains': lambda o: len(o),
    }

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        defaultdict.__init__(self, lambda: FilepathsMaps())
        HasRecord.__init__(self, name='DomainFilepaths')
