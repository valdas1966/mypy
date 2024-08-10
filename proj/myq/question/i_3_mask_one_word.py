from proj.myq.question.i_2_mask import QuestionMask
from f_utils.dtypes.u_str import UStr as u_str


class QuestionMaskOneWord(QuestionMask):
    """
    ============================================================================
     QuestionText with one random word Masked-Answer.
    ============================================================================
    """

    def _mask_answer(self) -> str:
        """
        ========================================================================
         Return Masked-Answer.
        ========================================================================
        """
        return u_str.mask.one_word(text=self.answer, pct=self.pct_mask)
