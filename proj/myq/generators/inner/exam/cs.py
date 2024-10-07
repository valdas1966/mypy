from proj.myq.exams.i_0_base import ExamBase
from proj.myq.gsheets.cs.i_0_cs import SheetCS, QuestionMaskOneWord


class CS:

    @staticmethod
    def base() -> ExamBase[QuestionMaskOneWord]:
        """
        ========================================================================
         Generate Base CS-Exam (all questions).
        ========================================================================
        """
        qs = SheetCS().to_questions()
        return ExamBase(qs=qs)
