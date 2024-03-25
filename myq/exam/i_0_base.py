from myq.question.i_0_base import QuestionBase as Question


class ExamBase:
    """
    ============================================================================
     Base Exam-Class.
    ============================================================================
    """

    def __init__(self, qs: list[Question]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._qs = qs

    @property
    # List of Exam's Questions
    def questions(self) -> list[Question]:
        return self._qs
