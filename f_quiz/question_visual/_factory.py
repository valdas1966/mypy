from f_quiz.question_visual.main import QuestionVisual


class Factory:
    """
    ============================================================================
     Factory for QuestionVisual.
    ============================================================================
    """

    @staticmethod
    def argument_anatomy() -> QuestionVisual:
        """
        ========================================================================
         Visual: structure of an Argument (Premise 1, Premise 2, ?).
        ========================================================================
        """
        return QuestionVisual(
            topic='Argument Anatomy',
            svg_path='Quiz/Visuals/01_argument_anatomy.svg',
            masked_label='?',
            answer='Conclusion',
            wrong='Premise',
        )

    @staticmethod
    def modus_ponens() -> QuestionVisual:
        """
        ========================================================================
         Visual: Modus Ponens template (If P then Q; P; therefore ?).
        ========================================================================
        """
        return QuestionVisual(
            topic='Modus Ponens',
            svg_path='Quiz/Visuals/04_modus_ponens.svg',
            masked_label='?',
            answer='Q',
            wrong='P',
        )
