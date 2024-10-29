from f_proj.myq.gsheets.i_1_group import SheetGroup
from f_proj.myq.questions.i_3_mask_one_word import (QuestionMaskOneWord as
                                                    Question)


class SheetCS(SheetGroup):
    """
    ============================================================================
     Computer-Science Sheet in the Myq-Project.
    ============================================================================
    """

    _ID_SPREAD = '1haZi5T98P6kq3dnq4dO10JHDql-179B1oVluxQ_CW2M'
    _EXCLUDE = {'latin', 'greek', '1960s', '1970s'}

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetGroup.__init__(self,
                            id_spread=SheetCS._ID_SPREAD,
                            type_question=Question,
                            exclude=SheetCS._EXCLUDE)
