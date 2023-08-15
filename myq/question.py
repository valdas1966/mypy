from myq.comps.question.stats import QuestionStats


class Question:
    """
    ============================================================================
     Desc: Represents a Question.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. text (str)               : Question's Text.
        2. answer (str)             : Question's Answer.
        3. stats (QuestionStats)    : Question's Statistics.
    ============================================================================
    """

    def __init__(self,
                 text: str,          # Question's Text
                 answer: str         # Question's Answer
                 ) -> None:
        self._text = text
        self._answer = answer
        self._stats = QuestionStats()

    @property
    def text(self) -> str:
        return self._text

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def stats(self) -> QuestionStats:
        return self._stats
