from f_quiz.question import Question
from f_quiz.loaders.u_gsheet import load
from f_quiz.exam.main import Exam


class Factory:
    """
    ========================================================================
     Factory for Exam.
    ========================================================================
    """

    @staticmethod
    def two_capitals() -> Exam:
        """
        ====================================================================
         Create an Exam with two capital city Questions.
        ====================================================================
        """
        questions = [
            Question.Factory.capital_of_france(),
            Question.Factory.capital_of_germany()
        ]
        return Exam(questions=questions)

    @staticmethod
    def hebrew() -> Exam:
        """
        ====================================================================
         Create an Exam from the Hebrew Google Sheet.
        ====================================================================
        """
        return Exam(questions=load(sheet_name='Hebrew'))
