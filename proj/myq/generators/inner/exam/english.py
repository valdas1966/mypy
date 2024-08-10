from proj.myq.exam.i_1_random import ExamRandom, QuestionBase
from proj.myq.exam.u_2_combine import ExamCombine
from proj.myq.gsheets.english.i_1_phrases import SheetPhrases
from proj.myq.gsheets.english.i_1_definitions import SheetDefinitions
from typing import Generic, TypeVar

Q = TypeVar('Q', bound=QuestionBase)


class English(Generic[Q]):
    """
    ============================================================================
     Inner-Class for generating exams in English.
    ============================================================================
    """

    @staticmethod
    def combine(cnt_phrases: int,
                cnt_definitions: int) -> ExamCombine[Q]:
        """
        ========================================================================
         Generate combined English-Exam.
        ========================================================================
        """
        exam_phrases = English.phrases(cnt=cnt_phrases)
        exam_definitions = English.definitions(cnt=cnt_definitions)
        exams = [exam_phrases, exam_definitions]
        return ExamCombine(exams=exams)

    @staticmethod
    def phrases(cnt: int) -> ExamRandom[Q]:
        """
        ========================================================================
         Generate Exam of English-Phrases.
        ========================================================================
        """
        qs = SheetPhrases().to_questions()
        return ExamRandom(qs=qs, cnt=cnt)

    @staticmethod
    def definitions(cnt: int) -> ExamRandom[Q]:
        """
        ========================================================================
         Generate Exam of English-Definitions.
        ========================================================================
        """
        qs = SheetDefinitions().to_questions()
        return ExamRandom(qs=qs, cnt=cnt)
