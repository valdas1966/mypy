from f_proj.myq.gsheets.i_1_group import SheetGroup
from f_proj.myq.questions.i_3_mask_one_word import QuestionMaskOneWord


class SheetCS(SheetGroup[QuestionMaskOneWord]):
    """
    ============================================================================
     Computer-Science Sheet in the Myq-Project.
    ============================================================================
    """

    _ID_SPREAD = '1haZi5T98P6kq3dnq4dO10JHDql-179B1oVluxQ_CW2M'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SheetGroup.__init__(self,
                            id_spread=SheetCS._ID_SPREAD,
                            type_question=QuestionMaskOneWord)
