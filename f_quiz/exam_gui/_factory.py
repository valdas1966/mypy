from f_quiz.question import Question
from f_quiz.loaders.u_gsheet import load
from f_quiz.exam_gui.main import ExamGui


class Factory:
    """
    ========================================================================
     Factory for ExamGui.
    ========================================================================
    """

    @staticmethod
    def two_capitals() -> ExamGui:
        """
        ====================================================================
         Create an ExamGui with two capital city Questions.
        ====================================================================
        """
        questions = [
            Question.Factory.capital_of_france(),
            Question.Factory.capital_of_germany()
        ]
        return ExamGui(questions=questions)

    @staticmethod
    def hebrew() -> ExamGui:
        """
        ====================================================================
         Create an ExamGui from the Hebrew Google Sheet.
        ====================================================================
        """
        return ExamGui(questions=load(sheet_name='Hebrew'))

    @staticmethod
    def hebrew_random(n_questions: int | None = None) -> ExamGui:
        """
        ====================================================================
         Create a randomized ExamGui from the Hebrew Google Sheet.
        ====================================================================
        """
        return ExamGui(questions=load(sheet_name='Hebrew'),
                       is_random=True,
                       n_questions=n_questions)
