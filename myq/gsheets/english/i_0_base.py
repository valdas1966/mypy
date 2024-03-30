from f_google.sheets.client import GSheets
from myq.gsheets import keys
from abc import ABC


class SheetBase(ABC):
    """
    ============================================================================
     Abstract-Class for Sheet in Myq-English.
    ============================================================================
    """

    # Name of the Myq-Spread
    __NAME_SPREAD = 'English'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        id_spread = keys.get(name_spread=SheetBase.__NAME_SPREAD)
        self._spread = GSheets.spread(user='VALDAS',
                                      id_spread=id_spread)
