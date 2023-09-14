
class QuestionStats:
    """
    ============================================================================
     Desc: Question's Statistics.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. asked (int)          : Number of times the Question was asked.
        2. answered (int)       : Number of times the Question was answered
                                   correctly.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. pct_answered() -> float
           [*] Percentage of correct answers.
        2. update(is_true: bool) -> None
           [*] Updates the Stats based on the answer being correct (is_true).
    ============================================================================
    """

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
        if not self.asked:
            return 0
        return self.answered / self.asked

    def update(self, is_true: bool) -> None:
        """
        ========================================================================
         Desc: Updates the Stats based on the answer being correct (is_true).
        ========================================================================
        """
        self._asked += 1
        self._answered += int(is_true)
