from myq.inner.question.i_1_text import QuestionText
from f_abstract.mixins.inputable import Inputable


class QuestionInputable(QuestionText, Inputable):
    """
    ============================================================================
     Extends QuestionText to display a Question to the User and captures
      its answer.
    ============================================================================
    """

    def __init__(self, text: str, answer: str) -> None:
        QuestionText.__init__(self, text, answer)
        Inputable.__init__(self)
