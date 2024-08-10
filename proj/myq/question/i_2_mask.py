from proj.myq.question.i_1_text import QuestionText
from f_utils.dtypes.u_str import UStr as u_str


class QuestionMask(QuestionText):
    """
    ============================================================================
     QuestionText with Masked-Answer.
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 answer: str,
                 pct_mask: int = 100) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        QuestionText.__init__(self, text=text, answer=answer)
        self._pct_mask = pct_mask
        self._answer_mask = self._mask_answer()

    @property
    def pct_mask(self) -> int:
        """
        ========================================================================
         Return percentage of masked chars in Masked-Answer.
        ========================================================================
        """
        return self._pct_mask

    @property
    def answer_mask(self) -> str:
        """
        ========================================================================
         Return a Masked-Answer.
        ========================================================================
        """
        return self._answer_mask

    def _mask_answer(self) -> str:
        """
        ========================================================================
         Return Masked-Answer.
        ========================================================================
        """
        return u_str.mask.full(s=self.answer)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr in format: 'Question -> Masked-Answer -> Right-Answer'.
        ========================================================================
        """
        return f'{self._text} -> {self.answer_mask} -> {self.answer}'
