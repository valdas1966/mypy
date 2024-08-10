from proj.myq.gsheets.english.i_1_phrases import SheetPhrases
from proj.myq.gsheets.english.i_1_definitions import SheetDefinitions
from proj.myq.question.i_1_text import QuestionText


class UEnglish:
    """
    ============================================================================
     Utils-Class for generating English-Questions.
    ============================================================================
    """

    @staticmethod
    def all() -> list[QuestionText]:
        """
        ========================================================================
         Return list of all English-Questions.
        ========================================================================
        """
        qs_phrases = SheetPhrases().to_questions()
        qs_definitions = SheetDefinitions().to_questions()
        return qs_phrases + qs_definitions
