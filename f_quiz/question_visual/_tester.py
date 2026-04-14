from f_quiz.question_visual import QuestionVisual


def test_factory_argument_anatomy() -> None:
    """
    ========================================================================
     Test the Factory.argument_anatomy() method.
    ========================================================================
    """
    q = QuestionVisual.Factory.argument_anatomy()
    assert q.answer == 'Conclusion'
    assert q.wrong == 'Premise'
    assert q.svg_path.endswith('01_argument_anatomy.svg')
    assert set(q.options) == {'Conclusion', 'Premise'}


def test_factory_modus_ponens() -> None:
    """
    ========================================================================
     Test the Factory.modus_ponens() method.
    ========================================================================
    """
    q = QuestionVisual.Factory.modus_ponens()
    assert q.answer == 'Q'
    assert q.wrong == 'P'
    assert 'Modus Ponens' in q.text
