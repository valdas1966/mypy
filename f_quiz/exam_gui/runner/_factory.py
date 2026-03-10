from f_quiz.question import Question
from f_quiz.exam_gui.runner.main import ExamRunner


class Factory:
    """
    ========================================================================
     Factory for ExamRunner.
    ========================================================================
    """

    @staticmethod
    def two_capitals() -> ExamRunner:
        """
        ====================================================================
         Create an ExamRunner with two capital city Questions.
        ====================================================================
        """
        questions = [
            Question.Factory.capital_of_france(),
            Question.Factory.capital_of_germany()
        ]
        return ExamRunner(questions=questions)

    @staticmethod
    def two_capitals_random() -> ExamRunner:
        """
        ====================================================================
         Create a randomized ExamRunner with two capital city Questions.
        ====================================================================
        """
        questions = [
            Question.Factory.capital_of_france(),
            Question.Factory.capital_of_germany()
        ]
        return ExamRunner(questions=questions, is_random=True)

    @staticmethod
    def two_capitals_n(n_questions: int) -> ExamRunner:
        """
        ====================================================================
         Create an ExamRunner limited to N Questions.
        ====================================================================
        """
        questions = [
            Question.Factory.capital_of_france(),
            Question.Factory.capital_of_germany()
        ]
        return ExamRunner(questions=questions, n_questions=n_questions)
