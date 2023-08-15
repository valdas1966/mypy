
class QuestionStats:
    """
    ============================================================================
     Desc: Question-Component for Statistics.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. asked (int)          : Times the Question was asked.
        2. answered (int)       : Times the Question was answered correctly.
        3. pct_answered (int)   : Correct answer Percentage.
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

    @property
    def pct_answered(self) -> int:
        if not self.asked:
            return 0
        return int(self.answered / self.asked * 100)
