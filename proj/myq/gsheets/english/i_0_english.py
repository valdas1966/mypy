from abc import ABC, abstractmethod
from f_google.sheets.client import GSheets
from proj.myq.question.i_1_text import QuestionText as Q


class SheetEnglish(ABC):
    """
    ============================================================================
     Abstract-Class for Sheet in Myq-English.
    ============================================================================
    """

    _ID_SPREAD = '1mOhkn4DPpUlgtuQxzTPNWlymBSmq9fS7T0t3IaDFf98'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._spread = GSheets.spread(user='VALDAS',
                                      id_spread=self._ID_SPREAD)
