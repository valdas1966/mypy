from f_proj.myq.exams.i_0_base import ExamBase
from f_proj.myq.gsheets.cs.i_0_cs import SheetCS, QuestionMaskOneWord
from f_ds.groups.nested import NestedGroup


class CS:
    """
    ============================================================================
     Computer-Science exams in the Myq-Project.
    ============================================================================
    """

    @staticmethod
    def base() -> ExamBase[QuestionMaskOneWord]:
        """
        ========================================================================
         Generate Base CS-Exam (all questions).
        ========================================================================
        """
        groups = SheetCS().to_nested_group()
        return ExamBase(qs=qs)
