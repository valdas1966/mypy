from proj.myq.exam.i_1_random import ExamRandom
from proj.myq.question.i_1_text import QuestionText
from proj.myq.gsheets.english.i_1_phrases import SheetPhrases


class English:
    """
    ============================================================================
     Inner-Class for generating exams in English.
    ============================================================================
    """

    @staticmethod
    def phrases(cnt: int) -> ExamRandom:
        """
        ========================================================================
         Generate Exam of English-Phrases.
        ========================================================================
        """
        qs = SheetPhrases().to_questions()
        return ExamRandom[QuestionText](qs=qs, cnt=cnt)
