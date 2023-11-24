
class QuestionBase:
    """
    ============================================================================
     Manages basic statistics related to a question.
    ============================================================================
    """

    def __init__(self) -> None:
        self._asked = 0
        self._answered = 0

    @property
    # Number of times the Question was asked.
    def asked(self) -> int:
        return self._asked

    @property
    # Number of times the Question was answered correctly.
    def answered(self) -> int:
        return self._answered

    def pct_answered(self) -> float:
        """
        ========================================================================
         Returns the Percentage of correct answers.
        ========================================================================
        """
        if not self.asked:
            return 0
        return self.answered / self.asked

    def update(self, is_true: bool) -> None:
        """
        ========================================================================
         Updates the Stats based on the answer being correct (is_true).
        ========================================================================
        """
        self._asked += 1
        self._answered += int(is_true)
