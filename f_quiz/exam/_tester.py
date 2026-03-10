from f_quiz.exam import Exam


def test_questions() -> None:
    """
    ========================================================================
     Test that Exam stores the Questions.
    ========================================================================
    """
    exam = Exam.Factory.two_capitals()
    assert len(exam.questions) == 2
    assert exam.questions[0].text == 'Capital of France'
    assert exam.questions[1].text == 'Capital of Germany'


def test_run_correct(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with all correct answers.
    ========================================================================
    """
    answers = iter(['Paris', 'Berlin'])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    exam = Exam.Factory.two_capitals()
    exam.run()


def test_run_wrong(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with wrong answers.
    ========================================================================
    """
    answers = iter(['London', 'Madrid'])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    exam = Exam.Factory.two_capitals()
    exam.run()


def test_is_random(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with is_random=True shuffles Questions.
    ========================================================================
    """
    monkeypatch.setattr('builtins.input', lambda _: 'skip')
    exam = Exam.Factory.two_capitals_random()
    # Verify all questions are present (order may vary)
    qs = exam._prepare_questions()
    texts = {q.text for q in qs}
    assert texts == {'Capital of France', 'Capital of Germany'}


def test_n_questions(monkeypatch) -> None:
    """
    ========================================================================
     Test run() with n_questions limits the number of Questions.
    ========================================================================
    """
    answers = iter(['Paris'])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))
    exam = Exam.Factory.two_capitals_n(n_questions=1)
    exam.run()
    assert len(exam._prepare_questions()) == 1
