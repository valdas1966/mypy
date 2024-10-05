from proj.myq.questions.i_0_base import QuestionBase
from f_abstract.mixins.printable import Printable


class QuestionText(QuestionBase, Printable):
    """
    ============================================================================
     Concrete-Class Text-Based Question (Question and Answer are Texts).
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 answer: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        QuestionBase.__init__(self)
        self._text = text
        self._answer = answer

    @property
    # Question's Text
    def text(self) -> str:
        return self._text

    @property
    # Question's right Answer
    def answer(self) -> str:
        return self._answer

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr in format: 'Question -> Right-Answer'.
        ========================================================================
        """
        return f'{self._text} -> {self.answer} {str(self.stats)}'
