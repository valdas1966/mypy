from abc import ABC
from f_google.sheets.client import GSheets


class SheetBase(ABC):
    """
    ============================================================================
     Abstract-Class for Sheet in Myq-English.
    ============================================================================
    """

    __ID_SPREAD = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = GSheets.spread(user='VALDAS',
                                      id_spread=SheetBase.__ID_SPREAD)
