from myq.inner.question.i_0_stats import QuestionStats


class QuestionText(QuestionStats):
    """
    ============================================================================
     Text-Based Question (both Question and the Answer are Texts).
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 answer: str) -> None:
        QuestionStats.__init__(self)
        self._text = text
        self._answer = answer

    @property
    # Question's Text
    def text(self) -> str:
        return self._text

    @property
    # Question's Answer
    def answer(self) -> str:
        return self._answer

    def __str__(self) -> str:
        return f'{self._text} -> {self.answer}'

    def __repr__(self) -> str:
        return self.__str__()
