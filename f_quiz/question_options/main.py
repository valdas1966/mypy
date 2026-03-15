import random

from f_quiz.question.main import Question


class QuestionOptions(Question):
    """
    ========================================================================
     Quiz Question with two Answer Options (correct and wrong).
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 text: str,
                 answer: str,
                 wrong: str) -> None:
        """
        ====================================================================
         Init with Text, correct Answer, and wrong Option.
        ====================================================================
        """
        Question.__init__(self, text=text, answer=answer)
        self._wrong = wrong

    @property
    def wrong(self) -> str:
        """
        ====================================================================
         Return the wrong Option.
        ====================================================================
        """
        return self._wrong

    @property
    def options(self) -> list[str]:
        """
        ====================================================================
         Return [answer, wrong] in random order.
        ====================================================================
        """
        opts = [self._answer, self._wrong]
        random.shuffle(opts)
        return opts

    def __str__(self) -> str:
        return f'{self._text} -> {self._answer} | {self._wrong}'
