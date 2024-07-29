from proj.myq.exam.i_1_random import ExamRandom
from proj.myq.question.i_1_text import QuestionText
from proj.myq.gsheets.english.i_1_phrases import SheetPhrases


class UtilsExamRandom:
    """
    ============================================================================
     Utils-Class to generate Random-Exams.
    ============================================================================
    """

    @staticmethod
    def phrases() -> ExamRandom:
        questions = SheetPhrases().to_questions()
        return ExamRandom(qs=questions, cnt=10)
