from f_data_structure.collections.priority_queue import PriorityQueue


def test_init():
    q = PriorityQueue()
    assert not q
    assert len(q) == 0


def test_push():
    q = PriorityQueue()
    q.push(1)
    assert q
    assert len(q) == 1


def test_pop():
    q = PriorityQueue()
    q.push(3)
    q.push(1)
    q.push(2)
    assert q.pop() == 1
    assert len(q) == 2
