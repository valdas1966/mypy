from f_quiz.question_options.main import QuestionOptions


class QuestionVisual(QuestionOptions):
    """
    ============================================================================
     Quiz Question backed by a Diagram (SVG) with one masked Label.
    ============================================================================
    """

    Factory: type = None

    def __init__(self,
                 topic: str,
                 svg_path: str,
                 masked_label: str,
                 answer: str,
                 wrong: str) -> None:
        """
        ========================================================================
         Init with Topic, Drive SVG Path, the masked Label (for debug/prompt),
         the correct Answer, and the wrong Option.
        ========================================================================
        """
        text = f'[{topic}] Fill the missing label: {masked_label}'
        QuestionOptions.__init__(self, text=text, answer=answer, wrong=wrong)
        self._topic = topic
        self._svg_path = svg_path
        self._masked_label = masked_label

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def svg_path(self) -> str:
        return self._svg_path

    @property
    def masked_label(self) -> str:
        return self._masked_label

    def __str__(self) -> str:
        return (f'{self._topic} [{self._svg_path}] '
                f'-> {self._answer} | {self._wrong}')
