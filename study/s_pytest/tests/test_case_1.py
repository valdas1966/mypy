import study.s_pytest.case_1 as case_1


def test_sum():
    assert case_1.sum(1, 1) == 2
    assert case_1.sum(1, 2) == 3
    assert case_1.sum(2, 2) == 5
