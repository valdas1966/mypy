from proj.myq.exams.i_1_random import ExamRandom
from proj.myq.gsheets.english.u_english import UEnglish as u_english


class UtilsExamRandom:
    """
    ============================================================================
     Utils-Class to generate Random-Exams.
    ============================================================================
    """

    @staticmethod
    def english(cnt: int = 10) -> ExamRandom:
        questions = u_english.all()
        return ExamRandom(qs=questions, cnt=cnt)
