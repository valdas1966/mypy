from myq.inner.question.i_0_base import QuestionStats


def test_pct_answered():
    q = QuestionStats()
    assert q.pct_answered() == 0
    q.update(True)
    assert q.pct_answered() == 1
    q.update(False)
    assert q.pct_answered() == 0.5
