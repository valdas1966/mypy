
class QuestionText:
    """
    ============================================================================
     Desc: Text-Based Question.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. text (str)       : Question's Text.
        2. answer (str)     : Question's Answer.
    ============================================================================
    """

    def __init__(self,
                 text: str,
                 answer: str) -> None:
        self._text = text
        self._answer = answer

    @property
    def text(self) -> str:
        return self._text

    @property
    def answer(self) -> str:
        return self._answer

    def __str__(self) -> str:
        return f'{self._text} -> {self.answer}'
