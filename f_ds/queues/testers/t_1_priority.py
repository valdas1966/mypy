from f_ds.queues.i_1_priority import QueuePriority


def test_priority():
    q = QueuePriority()
    q.push(element=2)
    q.push(element=1)
    assert q.pop() == 1
