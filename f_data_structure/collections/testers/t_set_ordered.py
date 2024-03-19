from f_data_structure.collections.set_ordered import SetOrdered


def test_set_ordered():
    s = SetOrdered()
    s.add(element=2)
    s.add(element=1)
    assert list(s) == [2, 1]
