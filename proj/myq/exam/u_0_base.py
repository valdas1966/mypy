from proj.myq.exam.i_0_base import ExamBase
from proj.myq.question.i_1_text import QuestionText
from proj.myq.gsheets.english.i_1_phrases import SheetPhrases


class UtilsExamBase:

    @staticmethod
    def stam() -> ExamBase:
        qs = [QuestionText(text=f'Q{i}', answer=str()) for i in range(1, 3)]
        return ExamBase(qs=qs)

    @staticmethod
    def phrases() -> ExamBase:
        questions = SheetPhrases().to_questions()
        return ExamBase(qs=questions)
