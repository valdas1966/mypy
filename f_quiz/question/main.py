class Question:
    """
    ========================================================================
     Quiz Question with Text and Answer.
    ========================================================================
    """

    Factory: type = None

    def __init__(self, text: str, answer: str) -> None:
        """
        ====================================================================
         Init with Text and Answer.
        ====================================================================
        """
        self._text = text
        self._answer = answer

    @property
    def text(self) -> str:
        """
        ====================================================================
         Return the Question Text.
        ====================================================================
        """
        return self._text

    @property
    def answer(self) -> str:
        """
        ====================================================================
         Return the Answer.
        ====================================================================
        """
        return self._answer

    def __str__(self) -> str:
        return f'{self._text} -> {self._answer}'
