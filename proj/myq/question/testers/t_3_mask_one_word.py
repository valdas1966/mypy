from proj.myq.question.i_3_mask_one_word import QuestionMaskOneWord


def test_mask():
    q = QuestionMaskOneWord(text='Q', answer='a b')
    assert q.answer_mask in ('* b', 'a *')
