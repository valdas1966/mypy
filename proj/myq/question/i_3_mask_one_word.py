from proj.myq.question.i_2_mask import QuestionMask
from f_utils.dtypes.u_str import UStr as u_str


class QuestionMaskOneWord(QuestionMask):
    """
    ============================================================================
     QuestionText with one random word Masked-Answer.
    ============================================================================
    """

    def _set_private_attributes(self) -> None:
        """
        ========================================================================
         Return Masked-Answer.
        ========================================================================
        """
        hint, answer = u_str.mask.one_word(text=self.answer,
                                           pct=self.pct_mask)
        self._hint = hint.lower()
        self._answer = answer.lower()