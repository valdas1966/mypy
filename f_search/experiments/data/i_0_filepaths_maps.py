from collections import UserList
from f_core.mixins.has.record import HasRecord


class FilepathsMaps(UserList[str], HasRecord):
    """
    ============================================================================
     FilepathsMaps is a list of filepaths to maps.
    ============================================================================
    """

    RECORD_SPEC = {
        'filepaths': lambda o: len(o),
    }

    def __init__(self, filepaths: list[str] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        filepaths = filepaths or []
        UserList.__init__(self, filepaths)
        HasRecord.__init__(self, name='FilepathsMaps')
