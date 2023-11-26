from myq.question import Question


class ExamBase:
    """
    ============================================================================
     Base Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: list[Question]) -> None:
        self._qs = qs

    @property
    # List of Exam's Questions
    def questions(self) -> list[Question]:
        return self._qs
