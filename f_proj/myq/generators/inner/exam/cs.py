from f_proj.myq.exams.i_0_base import ExamBase
from f_proj.myq.gsheets.cs.i_0_cs import SheetCS, Question


class CS:
    """
    ============================================================================
     Computer-Science exams in the Myq-Project.
    ============================================================================
    """

    @staticmethod
    def base() -> ExamBase[Question]:
        """
        ========================================================================
         Generate Base CS-Exam (all questions).
        ========================================================================
        """
        groups = SheetCS().to_nested_group()
        groups_random = groups.sample(size=5)
        qs = [q for group in groups_random for q in group]
        return ExamBase(qs=qs)
