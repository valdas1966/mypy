
class QuestionStats:
    """
    ============================================================================
     Manages statistics related to a question.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. pct_answered() -> float
           [*] Percentage of correct answers.
        2. update(is_true: bool) -> None
           [*] Updates the Stats based on the answer being correct (is_true).
    ============================================================================
    """

    asked: int         # Number of times the Question was asked.
    answered: int      # Number of times the Question was answered correctly.

    def __init__(self) -> None:
        self._asked = 0
        self._answered = 0

    @property
    def asked(self) -> int:
        return self._asked

    @property
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
