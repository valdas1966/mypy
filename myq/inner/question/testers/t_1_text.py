from myq.inner.question.i_1_text import QuestionText


def test_str():
    q = QuestionText(text='a', answer='b')
    assert str(q) == 'a -> b'
    