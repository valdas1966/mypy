
class QuestionText:
    """
    ============================================================================
     Desc: Question-Component for Text-Based Questions.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. text (str) : Question's Text.
    ============================================================================
    """

    def __init__(self, text: str) -> None:
        self._text = text

    @property
    def text(self) -> str:
        return self._text
