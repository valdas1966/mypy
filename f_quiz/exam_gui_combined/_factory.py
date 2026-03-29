from f_quiz.exam_gui_combined.main import ExamGuiCombined
from f_quiz.question import Question
from f_quiz.question_options import QuestionOptions
from f_quiz.loaders.u_gsheet import load, load_options, load_yes_no


class Factory:
    """
    ========================================================================
     Factory for ExamGuiCombined.
    ========================================================================
    """

    @staticmethod
    def test() -> ExamGuiCombined:
        """
        ====================================================================
         Create with two text + two options Questions.
        ====================================================================
        """
        questions: list[Question] = [
            Question.Factory.capital_of_france(),
            QuestionOptions.Factory.logic(),
            Question.Factory.capital_of_germany(),
            QuestionOptions.Factory.formal()
        ]
        return ExamGuiCombined(questions=questions)

    @staticmethod
    def combined(is_random: bool = True,
                 n_questions: int | None = None
                 ) -> ExamGuiCombined:
        """
        ====================================================================
         Create from Hebrew + Options Google Sheets.
        ====================================================================
        """
        questions: list[Question] = (load(sheet_name='Hebrew')
                                     + load_options()
                                     + load_yes_no())
        return ExamGuiCombined(questions=questions,
                               is_random=is_random,
                               n_questions=n_questions)
