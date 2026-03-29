from f_quiz.exam_gui_options.main import ExamGuiOptions
from f_quiz.question_options import QuestionOptions
from f_quiz.loaders.u_gsheet import load_options, load_yes_no


class Factory:
    """
    ========================================================================
     Factory for ExamGuiOptions.
    ========================================================================
    """

    @staticmethod
    def logic() -> ExamGuiOptions:
        """
        ====================================================================
         Create an ExamGuiOptions with Logic definition Questions.
        ====================================================================
        """
        questions = [
            QuestionOptions.Factory.logic(),
            QuestionOptions.Factory.formal()
        ]
        return ExamGuiOptions(questions=questions)

    @staticmethod
    def options(sheet_name: str = 'Options',
                is_random: bool = True,
                n_questions: int | None = None) -> ExamGuiOptions:
        """
        ====================================================================
         Create an ExamGuiOptions from a Google Sheet.
        ====================================================================
        """
        return ExamGuiOptions(
            questions=load_options(sheet_name=sheet_name),
            is_random=is_random,
            n_questions=n_questions
        )

    @staticmethod
    def yes_no(is_random: bool = True,
               n_questions: int | None = None) -> ExamGuiOptions:
        """
        ====================================================================
         Create an ExamGuiOptions from the YesNo Google Sheet.
        ====================================================================
        """
        return ExamGuiOptions(
            questions=load_yes_no(),
            is_random=is_random,
            n_questions=n_questions
        )
