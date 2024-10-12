from f_proj.myq.questions.i_2_mask import QuestionMask


def test_mask():
    q = QuestionMask(text='2+2', answer='4', pct_mask=90)
    assert str(q) == '2+2 -> * -> 4'
