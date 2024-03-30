from myq.gsheets.english.i_0_base import SheetBase


class SheetWords(SheetBase):
    """
    ============================================================================
     Sheet for English-Words in the Myq project.
    ============================================================================
    """

    __NAME_SHEET = 'Words'

    __COL_QUESTION = 2
    __COL_ANSWER = 3

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetBase.__init__(self)
        self._sheet = self._spread[SheetWords.__NAME_SHEET]
