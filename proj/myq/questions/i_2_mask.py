from proj.myq.questions.i_1_text import QuestionText
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
        self._hint = None
        self._set_private_attributes()

    @property
    def pct_mask(self) -> int:
        """
        ========================================================================
         Return percentage of masked chars in Masked-Answer.
        ========================================================================
        """
        return self._pct_mask

    @property
    def hint(self) -> str:
        """
        ========================================================================
         Return a Masked-Answer.
        ========================================================================
        """
        return self._hint

    def _set_private_attributes(self) -> None:
        """
        ========================================================================
         Set private Attributes.
        ========================================================================
        """
        self._hint = u_str.mask.full(s=self.answer)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr in format: 'Question -> Masked-Answer -> Right-Answer'.
        ========================================================================
        """
        return f'{self._text} -> {self.hint} -> {self.answer}'
